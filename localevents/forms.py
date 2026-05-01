from django import forms
from .models import EventSignup

class GuestSignupForm(forms.ModelForm):
    class Meta:
        model = EventSignup
        fields = ['new_registrant']