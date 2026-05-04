from django.views.generic import ListView
from django.views.generic.detail import DetailView

from .models import ProjectCategory, Project


class ProjectListView(ListView):
    context_object_name = 'projects'
    model = Project
    template_name = 'diyprojects/project_list.html' # default value

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.request.user.profile

        context['created'] = Project.objects.filter(creator=profile)
        context['favorited'] = Project.objects.filter(favorites__profile=profile)
        context['reviewed'] = Project.objects.filter(reviews__reviewer=profile)

        return context



class ProjectDetailView(DetailView):
    model = Project
    template_name = 'diyprojects/project_detail.html' # default value
    