from django import forms
from .models import Project, ProjectReview, ProjectRating, Favorite


class ProjectForm(forms.ModelForm):
    pass


class ProjectRatingForm(forms.ModelForm):
    class Meta:
        model = ProjectRating
        fields = ['score']