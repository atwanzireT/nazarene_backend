from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import (
    User,
    AccountApplication,
    Project,
    Activity,
    Event,
    EventRegistration,
    Notification
)

# Custom User Registration Form
class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'full_name', 'email', 'phone_number', 'password1', 'password2']


# Account Application Form
class AccountApplicationForm(forms.ModelForm):
    class Meta:
        model = AccountApplication
        fields = ['full_name', 'email', 'phone_number', 'course', 'year_of_graduation', 'message']


# Project Form
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'status', 'progress', 'start_date', 'end_date']


# Activity Form
class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['project', 'title', 'description', 'activity_date']


# Event Form
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'event_date', 'location', 'slots']


# Event Registration Form (User is set in the view)
class EventRegistrationForm(forms.ModelForm):
    class Meta:
        model = EventRegistration
        fields = ['event']


# Notification Form
class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['user', 'title', 'message', 'is_read']
