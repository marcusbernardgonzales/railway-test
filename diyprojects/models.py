from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# Temporary
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    short_bio = models.TextField()

    def __str__(self):
        return self.name

class ProjectCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('diyprojects:project_list')
    
    class Meta:
        ordering = ['name']
        verbose_name = "project category"
        verbose_name_plural = "project categories"


class Project(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        ProjectCategory,
        on_delete=models.SET_NULL,
        related_name = 'project_list',
        null=True,
        blank=True,
    )

    description = models.TextField()
    materials = models.TextField()
    steps = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('diyprojects:project_detail', args=[self.pk])
    
    class Meta:
        ordering = ['-created_on']


class Favorite(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name = "favorites"
    )
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name = 'favorites'
    )
    date_favorited = models.DateField()
    project_status = models.CharField(
        max_length=10,
        choices = [
            ('backlog', 'Backlog'),
            ('todo', 'To-Do'),
            ('done', 'Done'),
        ]
    )

    def __str__(self):
        return f"{self.profile} - {self.project}"


class ProjectReview(models.Model):
    reviewer = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name = 'project_reviews'
    )
    comment = models.TextField()
    image = models.ImageField(upload_to = 'images/', null=False, blank=True)

    def __str__(self):
        return f"{self.reviewer}: {self.comment}"


class ProjectRating(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name = 'project_ratings'
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='ratings',
        null=True,
        blank=True,
    )
    score = models.IntegerField()

    def __str__(self):
        return f"{self.profile} rating: {self.score}/10"    
