from django.urls import path

from .views import ProfileUpdateView

urlpatterns = [
    path('accounts/<str:username>/', ProfileUpdateView.as_view(), name='profile-update'),
]

app_name = "accounts"
