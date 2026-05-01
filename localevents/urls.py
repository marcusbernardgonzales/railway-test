from django.urls import path

from .views import *

urlpatterns = [
    path('localevents/events', EventListView.as_view(), name='event_list'),
    path('localevents/event/<int:pk>', EventDetailView.as_view(),
         name='event_detail'),
    path('localevents/event/add', EventCreateView.as_view(),
         name='event_create'),
    path('localevents/event/<int:pk>/edit', EventUpdateView.as_view(),
         name='event_edit'),
    path('localevents/event/<int:pk>/signup', EventSignupView.as_view(),
         name='event_signup'),
]

app_name = 'localevents'
