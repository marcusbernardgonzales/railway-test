from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render

from .models import Book, BookReview, Bookmark
from .forms import BookForm, BookReviewForm, BorrowForm


def is_book_contributor(user):
    return user.groups.filter(name='Book Contributors').exists()


class BookListView(ListView):
    model = Book
    template_name = 'bookclub/book_list.html'
    context_object_name = 'books'

    def get_queryset(self):
        qs = Book.objects.all()

        if self.request.user.is_authenticated and hasattr(self.request.user, 'profile'):
            profile = self.request.user.profile

            contributed = qs.filter(contributer=profile)
            bookmarked = qs.filter(bookmark__profile=profile)
            reviewed = qs.filter(bookreview__user_reviewer=profile)

            excluded_ids = (
                contributed.values_list('id', flat=True) |
                bookmarked.values_list('id', flat=True) |
                reviewed.values_list('id', flat=True)
            )

            qs = qs.exclude(id__in=excluded_ids)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated and hasattr(self.request.user, 'profile'):
            profile = self.request.user.profile

            context['contributed_books'] = Book.objects.filter(contributer=profile)
            context['bookmarked_books'] = Book.objects.filter(bookmark__profile=profile)
            context['reviewed_books'] = Book.objects.filter(bookreview__user_reviewer=profile)

        return context


class BookDetailView(DetailView):
    model = Book
    template_name = 'bookclub/book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        book = self.object
        user = self.request.user

        context['review_form'] = BookReviewForm()
        context['reviews'] = book.bookreview_set.all()
        context['bookmark_count'] = book.bookmark_set.count()
        context['available'] = book.available_to_borrow

        if user.is_authenticated and hasattr(user, 'profile'):
            context['is_bookmarked'] = Bookmark.objects.filter(
                profile=user.profile, book=book
            ).exists()

            context['can_edit'] = (book.contributer == user.profile)

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if 'submit_review' in request.POST:
            form = BookReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.book = self.object
                if request.user.is_authenticated and hasattr(request.user, 'profile'):
                    review.user_reviewer = request.user.profile
                else:
                    review.anon_reviewer = 'Anonymous'
                review.save()

        elif 'toggle_bookmark' in request.POST:
            if request.user.is_authenticated and hasattr(request.user, 'profile'):
                profile = request.user.profile
                bookmark = Bookmark.objects.filter(profile=profile, book=self.object)

                if bookmark.exists():
                    bookmark.delete()
                else:
                    Bookmark.objects.create(profile=profile, book=self.object)

        return redirect(self.object.get_absolute_url())


class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'bookclub/book_form.html'

    def dispatch(self, request, *args, **kwargs):
        if not is_book_contributor(request.user):
            return redirect('bookclub:book_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.contributor = self.request.user.profile
        return super().form_valid(form)


class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'bookclub/book_form.html'

    def dispatch(self, request, *args, **kwargs):
        book = self.get_object()

        if (
            not is_book_contributor(request.user)
            or book.contributor != request.user.profile
        ):
            return redirect('bookclub:book_list')

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.contributor = self.get_object().contributor
        return super().form_valid(form)


def borrow_book(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if not book.available_to_borrow:
        return redirect(book.get_absolute_url())

    if request.method == 'POST':
        form = BorrowForm(request.POST)
        if form.is_valid():
            borrow = form.save(commit=False)
            borrow.book = book

            if request.user.is_authenticated and hasattr(request.user, 'profile'):
                borrow.borrower = request.user.profile
                borrow.name = request.user.profile.display_name
            else:
                borrow.name = form.cleaned_data['name']

            borrow.save()

            book.available_to_borrow = False
            book.save()

            return redirect(book.get_absolute_url())

    else:
        if request.user.is_authenticated and hasattr(request.user, 'profile'):
            form = BorrowForm(initial={
                'name': request.user.profile.display_name
            })
            form.fields['name'].disabled = True
        else:
            form = BorrowForm()

    return render(request, 'bookclub/borrow_form.html', {'form': form, 'book': book})
