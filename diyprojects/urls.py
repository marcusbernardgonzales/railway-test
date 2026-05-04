from django.urls import path

from .views import ProjectListView, ProjectDetailView

app_name = 'diyprojects'

urlpatterns = [
    path('diyprojects/projects', ProjectListView.as_view(),
         name='project_list'),
    path('diyprojects/project/<int:pk>', ProjectDetailView.as_view(),
         name='project_detail'),
]
