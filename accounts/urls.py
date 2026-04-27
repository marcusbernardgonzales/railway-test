from django.urls import path
from .views import ProfileUpdateView

url_patterns = [
    path('<str:username>/', ProfileUpdateView.as_view(), name='profile-update'),
]

app_name = "accounts"
