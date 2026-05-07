from datetime import timedelta

from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404, redirect, render

from .models import Book, BookReview, Bookmark, Borrow
from .forms import BookForm, BookReviewForm, BorrowForm


def is_book_contributor(user):
    return ( 
        user.is_authenticated and 
        hasattr(user, "profile") and 
        (
        user.groups.filter(name="Commission Maker").exists() 
        or user.is_superuser 
        )
    )



class BookListView(ListView):
    model = Book
    template_name = 'bookclub/book_list.html'
    context_object_name = 'books'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated and hasattr(self.request.user, 'profile'):
            profile = self.request.user.profile

            contributed = Book.objects.filter(contributor=profile)

            bookmarked = Book.objects.filter(
                bookmark__profile=profile
            )

            reviewed = Book.objects.filter(
                bookreview__user_reviewer=profile
            )

            other = Book.objects.exclude(contributor=profile)
            other = other.exclude(bookmark__profile=profile)
            other = other.exclude(bookreview__user_reviewer=profile)

            context['contributed_books'] = contributed
            context['bookmarked_books'] = bookmarked
            context['reviewed_books'] = reviewed
            context['all_books'] = other

        else:
            context['all_books'] = Book.objects.all()

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
        
        is_owner = False

        if self.request.user.is_authenticated and hasattr(self.request.user, 'profile'):
            is_owner = book.contributor == self.request.user.profile
        
        context['is_owner'] = is_owner

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if 'bookmark' in request.POST:
            return self.handle_bookmark(request)

        if 'review' in request.POST:
            return self.handle_review(request)

        return redirect(self.object.get_absolute_url())
    
    def handle_bookmark(self, request):

        if request.user.is_authenticated and hasattr(request.user, 'profile'):

            Bookmark.objects.get_or_create(
                profile=request.user.profile,
                book=self.object
            )

        return redirect(self.object.get_absolute_url())
    
    def handle_review(self, request):

        form = BookReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)

            review.book = self.object

            if request.user.is_authenticated and hasattr(request.user, 'profile'):
                review.user_reviewer = request.user.profile
            else:
                review.anon_reviewer = 'Anonymous'

            review.save()

        return redirect(self.object.get_absolute_url())


class BaseBorrowView(View):

    def post(self, request, pk):

        book = get_object_or_404(Book, pk=pk)

        if not self.check_availability(book):
            return redirect(self.get_redirect_url(book))

        self.create_borrow(book, request)

        return redirect(self.get_redirect_url(book))

    def check_availability(self, book):
        raise NotImplementedError

    def create_borrow(self, book, request):
        raise NotImplementedError

    def get_redirect_url(self, book):
        raise NotImplementedError


class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'bookclub/book_form.html'

    def form_valid(self, form):
        if not is_book_contributor(self.request.user):
            return redirect('bookclub:book_list')

        form.instance.contributor = self.request.user.profile

        return super().form_valid(form)


class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'bookclub/book_form.html'
    context_object_name = 'book'

    def get(self, request, *args, **kwargs):

        book = self.get_object()

        if not is_book_contributor(request.user):
            return redirect('bookclub:book_list')

        if book.contributor != request.user.profile:
            return redirect('bookclub:book_detail', pk=book.pk)

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):

        book = self.get_object()

        if not is_book_contributor(self.request.user):
            return redirect('bookclub:book_list')

        if book.contributor != self.request.user.profile:
            return redirect('bookclub:book_detail', pk=book.pk)

        return super().form_valid(form)


class BookBorrowView(BaseBorrowView):
    def get(self, request, pk):

        book = get_object_or_404(Book, pk=pk)

        if request.user.is_authenticated and hasattr(request.user, 'profile'):
            form = BorrowForm(initial={
                'name': request.user.profile.display_name
            })

            form.fields['name'].disabled = True

        else:
            form = BorrowForm()

        return render(request, 'bookclub/borrow_form.html', {
            'form': form,
            'book': book
        })

    def check_availability(self, book):
        return book.available_to_borrow

    def create_borrow(self, book, request):

        form = BorrowForm(request.POST)

        if form.is_valid():

            borrow = form.save(commit=False)

            borrow.book = book

            if request.user.is_authenticated and hasattr(request.user, 'profile'):
                borrow.borrower = request.user.profile
                borrow.name = request.user.profile.display_name

            borrow.date_to_return = (
                borrow.date_borrowed + timedelta(days=14)
            )

            borrow.save()

            book.available_to_borrow = False
            book.save()

    def get_redirect_url(self, book):
        return book.get_absolute_url()
