from django import forms
from django.forms import inlineformset_factory
from .models import Commission, Job


class CommissionForm(forms.ModelForm):
    class Meta:
        model = Commission
        exclude = ['maker']


JobFormSet = inlineformset_factory(
    Commission,
    Job,
    fields=['role', 'manpower_required', 'status'],
    extra=1,
    can_delete=True
)
