from django.views.generic import ListView
from django.views.generic.detail import DetailView

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

        return context
