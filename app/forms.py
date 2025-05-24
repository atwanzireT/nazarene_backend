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
from .models import AccountApplication

class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            classes = 'form-control'
            if isinstance(field.widget, forms.Select):
                classes = 'form-select'
            field.widget.attrs.update({'class': classes})


class UserForm(BootstrapFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'full_name', 'email', 'phone_number', 'password1', 'password2']


class AccountApplicationForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = AccountApplication
        exclude = ['created_at', 'updated_at']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }


class ProjectForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'title', 'description', 'status', 'progress',
            'start_date', 'end_date', 'budget', 'raised_amount',
            'location', 'cover_image', 'is_featured'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }


class ActivityForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['project', 'title', 'description', 'activity_date', 'status', 'location', 'cover_image', 'notes']
        widgets = {
            'activity_date': forms.DateInput(attrs={'type': 'date'}),
        }


class EventForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'title', 'description', 'event_date', 'location', 'slots',
            'organizer', 'contact_email', 'contact_phone', 'status',
            'is_open', 'cover_image'
        ]
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'datetime-local'}),
        }


class EventRegistrationForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = EventRegistration
        fields = ['event']


class NotificationForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['user', 'title', 'message', 'is_read']


class AccountApplicationForm(forms.ModelForm):
    class Meta:
        model = AccountApplication
        fields = '__all__'
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
