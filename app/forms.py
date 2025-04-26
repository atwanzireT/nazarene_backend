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


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            classes = 'form-control'
            if isinstance(field.widget, forms.Select):
                classes = 'form-select'
            field.widget.attrs.update({'class': classes})


# Custom User Registration Form
class UserForm(BootstrapFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'full_name', 'email', 'phone_number', 'password1', 'password2']


# Account Application Form
class AccountApplicationForm(forms.ModelForm):
    class Meta:
        model = AccountApplication
        exclude = ['created_at', 'updated_at']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

# Project Form
class ProjectForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'status', 'progress', 'start_date', 'end_date', 'cover_image']
        
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }


# Activity Form
class ActivityForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['project', 'title', 'description', 'activity_date', 'cover_image']
        
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date'}),
        }

# Event Form
class EventForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'event_date', 'location', 'slots', 'cover_image']
        
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date'}),
        }


# Event Registration Form
class EventRegistrationForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = EventRegistration
        fields = ['event']


# Notification Form
class NotificationForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['user', 'title', 'message', 'is_read']
