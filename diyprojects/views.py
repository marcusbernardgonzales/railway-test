from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg
from django.shortcuts import redirect
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from .forms import ProjectRatingForm, ProjectReviewForm
from .models import Favorite, ProjectCategory, Project


class ProjectListView(ListView):
    model = Project
    template_name = 'diyprojects/project_list.html'
    context_object_name = 'projects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            
            created = Project.objects.filter(creator=profile)
            favorited = Project.objects.filter(favorites__profile=profile)
            reviewed = Project.objects.filter(reviews__reviewer=profile)
            
            context['created_projects'] = created
            context['favorited_projects'] = favorited
            context['reviewed_projects'] = reviewed

        return context


class ProjectDetailView(DetailView):
    context_object_name = 'project'
    model = Project
    template_name = 'diyprojects/project_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        ratings = project.ratings.all()

        average = ratings.aggregate(Avg('score'))['score__avg'] or 0
        favorite_count = project.favorites.count()

        reviews = project.reviews.all()

        context['avg_rating'] = average
        context['favorite_count'] = favorite_count
        context['rating_form'] = ProjectRatingForm()
        context['review_form'] = ProjectReviewForm()
        context['reviews'] = reviews

        if self.request.user.is_authenticated:
            profile = self.request.user.profile

            has_rated = project.ratings.filter(profile=profile).exists()
            is_favorited = project.favorites.filter(profile=profile).exists()
            is_owner = project.creator == profile

            context['has_rated'] = has_rated
            context['is_favorited'] = is_favorited
            context['is_owner'] = is_owner
        else:
            context['has_rated'] = False
        return context
    
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/admin/login/')
        
        self.object = self.get_object()
        profile = request.user.profile

        action = request.POST.get('action')

        if action == 'favorite':
            already = Favorite.objects.filter(
                profile=profile,
                project=self.object
            ).exists()

            if not already:
                Favorite.objects.create(
                    profile=profile,
                    project=self.object,
                    project_status='Backlog'
                )

        elif action == 'unfavorite':
            Favorite.objects.filter(
                profile=profile,
                project=self.object
            ).delete()

        elif action == 'rate':
            form = ProjectRatingForm(request.POST)
            if form.is_valid():
                rating = form.save(commit=False)
                rating.project = self.object
                rating.profile = profile
                rating.save()
        
        elif action == 'review':
            form = ProjectReviewForm(request.POST, request.FILES)
            if form.is_valid():
                review = form.save(commit=False)
                review.project = self.object
                review.reviewer = profile
                review.save()

        return redirect('diyprojects:project_detail', pk=self.object.pk)


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    fields = ['title', 'category', 'description', 'materials', 'steps']
    template_name = 'diyprojects/project_form.html'

    def form_valid(self, form):
        form.instance.creator = self.request.user.profile
        return super().form_valid(form)


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    fields = ['title', 'category', 'description', 'materials', 'steps']
    template_name = 'diyprojects/project_form.html'
