from django.urls import path

from .views import *

urlpatterns = [
    path('commissions/requests', CommissionListView.as_view(),
         name="commission_list"),
    path('commissions/request/<int:pk>', CommissionDetailView.as_view(),
         name="commission_detail"),
    path('commissions/request/add', CommissionCreateView.as_view(),
         name="commission_add"),
    path('commissions/request/<int:pk>/edit', CommissionUpdateView.as_view(),
         name="commission_edit"),
    path('commissions/job/<int:pk>/apply', ApplyToJobView.as_view(),
         name="job_apply"),
]

app_name = 'commissions'
