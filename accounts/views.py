from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView

from .models import Profile


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['display_name']
    template_name = 'accounts/profile_update.html'

    def get_object(self):
        return self.request.user.profile

    def get_success_url(self):
        return '/'
