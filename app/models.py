from django.contrib.auth.models import AbstractUser
from django.db import models

# Custom User Model
class User(AbstractUser):
    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    is_approved = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    REQUIRED_FIELDS = ['full_name', 'email']

    def __str__(self):
        return self.full_name

# Account Application (Old Student Request)
class AccountApplication(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    course = models.CharField(max_length=100)
    year_of_graduation = models.IntegerField()
    message = models.TextField(blank=True, null=True)
    is_reviewed = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.year_of_graduation})"

# Project & Activity
class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('ongoing', 'Ongoing'), ('completed', 'Completed')])
    progress = models.PositiveIntegerField(default=0)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title

class Activity(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='activities')
    title = models.CharField(max_length=200)
    description = models.TextField()
    activity_date = models.DateField()

    def __str__(self):
        return f"{self.project.title} - {self.title}"

# Events
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_date = models.DateTimeField()
    location = models.CharField(max_length=200)
    slots = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.title

# Event Registration
class EventRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')

# Notifications
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
