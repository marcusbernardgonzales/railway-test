from django.db import models
from django.urls import reverse

from accounts.models import Profile


class EventType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['name']
        verbose_name = 'event category'
        verbose_name_plural = 'event categories'

    def __str__(self):
        return self.name


class Event(models.Model):
    STATUS_CHOICES = {
        "Available": "Available",
        "Full": "Full",
        "Done": "Done",
        "Cancelled": "Cancelled",
    }

    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        EventType,
        on_delete=models.SET_NULL,
        related_name='events',
        null=True,
        blank=True,
    )
    organizer = models.ManyToManyField(Profile, blank=True)
    event_image = models.ImageField(upload_to='events/', blank=True, null=True)
    description = models.TextField()
    location = models.CharField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    event_capacity = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('localevents:event_detail', args=[int(self.pk)])

    class Meta:
        ordering = ['-created_on']
        verbose_name = 'event'
        verbose_name_plural = 'events'


class EventSignup(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
    )
    user_registrant = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    new_registrant = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.event.title
