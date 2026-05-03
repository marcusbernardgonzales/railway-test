from django import forms
from .models import Event, EventSignup

class GuestSignupForm(forms.ModelForm):
    class Meta:
        model = EventSignup
        fields = ['new_registrant']


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['organizer']