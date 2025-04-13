from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import (
    UserForm,
    AccountApplicationForm,
    ProjectForm,
    ActivityForm,
    EventForm,
    EventRegistrationForm,
    NotificationForm
)
from .models import Event, Project, Notification


def admin_required(view_func):
    return user_passes_test(lambda u: u.is_active and u.is_staff)(view_func)


@admin_required
def home(request):
    return render(request, 'home.html')

@admin_required
def register_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserForm()
    return render(request, 'register.html', {'form': form})


@admin_required
def apply_account(request):
    if request.method == 'POST':
        form = AccountApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AccountApplicationForm()
    return render(request, 'apply_account.html', {'form': form})


@admin_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'create_project.html', {'form': form})


@admin_required
def create_activity(request):
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ActivityForm()
    return render(request, 'create_activity.html', {'form': form})


@admin_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'create_event.html', {'form': form})


@admin_required
def register_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = EventRegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.user = request.user
            registration.event = event
            registration.save()
            return redirect('event_list')
    else:
        form = EventRegistrationForm(initial={'event': event})
    return render(request, 'register_event.html', {'form': form, 'event': event})


@admin_required
def create_notification(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = NotificationForm()
    return render(request, 'create_notification.html', {'form': form})
