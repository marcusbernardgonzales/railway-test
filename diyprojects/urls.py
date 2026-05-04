from django.urls import path

from .views import ProjectListView, ProjectDetailView, ProjectCreateView, ProjectUpdateView

app_name = 'diyprojects'

urlpatterns = [
    path('diyprojects/projects', ProjectListView.as_view(),
         name='project_list'),
    path('diyprojects/project/<int:pk>', ProjectDetailView.as_view(),
         name='project_detail'),
    path('diyprojects/project/add', ProjectCreateView.as_view(),
         name='project_add'),
    path('diyprojects/project/<int:pk>/edit', ProjectUpdateView.as_view(), 
         name='project_update')
]
