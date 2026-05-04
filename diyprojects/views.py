from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from .forms import ProjectRatingForm, ProjectReviewForm
from .models import ProjectCategory, Project


class ProjectListView(ListView):
    context_object_name = 'projects'
    model = Project
    template_name = 'diyprojects/project_list.html' # default value

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            context['created'] = Project.objects.filter(creator=profile)
            context['favorited'] = Project.objects.filter(favorites__profile=profile)
            context['reviewed'] = Project.objects.filter(reviews__reviewer=profile)

        return context


class ProjectDetailView(DetailView):
    context_object_name = 'project'
    model = Project
    template_name = 'diyprojects/project_detail.html' # default value

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        ratings = project.ratings.all()

        if ratings:
            context['avg_rating'] = sum(rating.score for rating in ratings) / ratings.count()
        else:
            context['avg_rating'] = 0
        
        context['favorite_count'] = project.favorites.count()
        context['rating_form'] = ProjectRatingForm()
        context['review_form'] = ProjectReviewForm()
        context['reviews'] = project.reviews.all()

        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            context['is_favorited'] = project.favorites.filter(profile=profile).exists()
            context['is_owner'] = project.creator == profile

        return context
    
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/admin/login/')
        
        self.object = self.get_object()
        profile = request.user.profile

        if 'score' in request.POST:
            form = ProjectRatingForm(request.POST)
            if form.is_valid():
                rating = form.save(commit=False)
                rating.project = self.object
                rating.profile = profile
                rating.save()
        
        elif 'comment' in request.POST:
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
