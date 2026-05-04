from django import forms
from .models import Project, ProjectReview, ProjectRating, Favorite


class ProjectForm(forms.ModelForm):
    pass