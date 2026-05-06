from django.db import models
from django.db.models import Case, When, Value, IntegerField
from django.urls import reverse

from accounts.models import Profile


class CommissionType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'commission type'
        verbose_name_plural = 'commission types'


class Commission(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Full', 'Full'),
        ('Completed', 'Completed'),
        ('Discontinued', 'Discontinued'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.ForeignKey(CommissionType, null=True, on_delete=models.SET_NULL)
    maker = models.ForeignKey(Profile, on_delete=models.CASCADE)
    people_required = models.PositiveIntegerField()
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='Open')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('commissions:commission_detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['created_on']
        verbose_name = 'commission'
        verbose_name_plural = 'commissions'


class Job(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Full', 'Full'),
    ]

    commission = models.ForeignKey(Commission, on_delete=models.CASCADE, related_name='jobs')
    role = models.CharField(max_length=255)
    manpower_required = models.PositiveIntegerField()
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='Open')

    class Meta:
        ordering = [
            Case(
                When(status='Open', then=Value(0)),
                When(status='Full', then=Value(1)),
                output_field=IntegerField(),
            ),
            '-manpower_required',
            'role'
        ]

    def __str__(self):
        return self.role


class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(Profile, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='Pending')
    applied_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = [
            Case(
                When(status='Accepted', then=0),
                When(status='Pending', then=1),
                When(status='Rejected', then=2),
                output_field=models.IntegerField(),
            ),
            '-applied_on'
        ]

    def __str__(self):
        return f"{self.applicant} - {self.job.role}"
