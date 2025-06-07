from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from .forms import *
from .models import *
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

User = get_user_model()

def admin_required(view_func):
    return login_required(user_passes_test(lambda u: u.role == 'ADMIN', login_url='/login/')(view_func))

# views.py
def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = EmailLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.role == user.Role.ADMIN:
                if user.is_approved:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, 'Your account is not approved yet.')
            else:
                messages.error(request, 'Only admin accounts are allowed to log in here.')
        else:
            messages.error(request, 'Invalid login credentials.')
    else:
        form = EmailLoginForm()

    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')


def notify_all_users(subject, message, fail_silently=False):
    """Send an email to all active users in the system using SendGrid."""
    users = User.objects.filter(is_active=True)
    recipient_list = [user.email for user in users if user.email]

    if not recipient_list:
        return 0

    try:
        # Send individual emails using SendGrid
        sg = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)

        for email in recipient_list:
            mail = Mail(
                from_email=settings.DEFAULT_FROM_EMAIL,
                to_emails=email,
                subject=subject,
                plain_text_content=message
            )
            sg.send(mail)

    except Exception as e:
        if not fail_silently:
            raise e
        # Optionally log the error here if needed
        return 0

    return len(recipient_list)


@admin_required
def home(request):
    user_activities = UserActivity.objects.all().order_by('-timestamp')[:10]
    context = {
        'total_users': User.objects.count(),
        'total_projects': Project.objects.count(),
        'total_activities': Activity.objects.count(),
        'total_events': Event.objects.count(),
        'user_activities':user_activities,
    }
    return render(request, 'home.html', context)


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
            project = form.save()
            
            # Notify all users about the new project
            subject = f"New Project: {project.title}"
            message = f"""
            A new project has been created!
            
            Title: {project.title}
            Description: {project.description}
            Start Date: {project.start_date}
            End Date: {project.end_date if project.end_date else 'Ongoing'}
            
            For more details, please log in to your account.
            """
            
            count = notify_all_users(subject, message)
            messages.success(request, f"Project created successfully. Notification sent to {count} users.")
            
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'create_project.html', {'form': form})


@admin_required
def create_activity(request):
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save()
            
            # Notify all users about the new activity
            subject = f"New Activity: {activity.title}"
            message = f"""
            A new activity has been created!
            
            Title: {activity.title}
            Project: {activity.project.title if activity.project else 'N/A'}
            Description: {activity.description}
            Date: {activity.date}
            Location: {activity.location}
            
            For more details, please log in to your account.
            """
            
            count = notify_all_users(subject, message)
            messages.success(request, f"Activity created successfully. Notification sent to {count} users.")
            
            return redirect('activity_list')
    else:
        form = ActivityForm()
    return render(request, 'create_activity.html', {'form': form})


@admin_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            
            # Notify all users about the new event
            subject = f"New Event: {event.title}"
            message = f"""
            A new event has been announced!
            
            Title: {event.title}
            Description: {event.description}
            Date: {event.date}
            Location: {event.location}
            Registration Deadline: {event.registration_deadline}
            
            For more details and to register, please log in to your account.
            """
            
            count = notify_all_users(subject, message)
            messages.success(request, f"Event created successfully. Notification sent to {count} users.")
            
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

# User list view
@admin_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

# Account Applications list view
@admin_required
def account_application_list(request):
    applications = AccountApplication.objects.filter(is_approved=False)
    return render(request, 'account_application_list.html', {'applications': applications})

@admin_required
def account_application_detail(request, application_id):
    application = get_object_or_404(AccountApplication, id=application_id)
    return render(request, 'account_application_detail.html', {'application': application})

# Project list view
@admin_required
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'project_list.html', {'projects': projects})

# Activity list view
@admin_required
def activity_list(request):
    activities = Activity.objects.select_related('project').all()
    return render(request, 'activity_list.html', {'activities': activities})

# Event list view
@admin_required
def event_list(request):
    events = Event.objects.all()
    return render(request, 'event_list.html', {'events': events})

# Event Registration list view
@admin_required
def event_registration_list(request):
    registrations = EventRegistration.objects.select_related('user', 'event').all()
    return render(request, 'event_registration_list.html', {'registrations': registrations})

# Notification list view
@admin_required
def notification_list(request):
    notifications = Notification.objects.select_related('user').all()
    return render(request, 'notification_list.html', {'notifications': notifications})



@login_required
def user_login_activities(request):
    activities = UserActivity.objects.filter(activity='login').order_by('-timestamp')
    return render(request, 'login_activities.html', {'activities': activities})


def account_application_create(request):
    if request.method == 'POST':
        form = AccountApplicationForm(request.POST)
        if form.is_valid():
            app = form.save()

            sg = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)

            try:
                # Admin notification email
                admin_email = Mail(
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to_emails=settings.ADMIN_EMAIL,
                    subject='New Account Application Submitted',
                    plain_text_content=(
                        f'New application from {app.full_first_name} {app.full_surname}\n'
                        f'Email: {app.email}\nPhone: {app.mobile_phone_1}\n'
                        f'Year Joined: {app.year_joined_jonahs}'
                    )
                )
                sg.send(admin_email)

                # Applicant confirmation email
                applicant_email = Mail(
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to_emails=app.email,
                    subject='Application Received',
                    plain_text_content=(
                        f'Dear {app.full_first_name},\n\n'
                        f'Thank you for submitting your application. We will review it shortly.\n\n'
                        f'Regards,\nThe Alumni Team'
                    )
                )
                sg.send(applicant_email)

                messages.success(request, "Application submitted successfully!")
                return redirect('account-application-success')

            except Exception as e:
                messages.warning(request, f"Application saved, but email failed to send: {e}")
                return redirect('account-application-success')

    else:
        form = AccountApplicationForm()

    return render(request, 'application_form.html', {'form': form})



@admin_required
def executive_team_list(request):
    members = ExecutiveTeamMember.objects.all()
    return render(request, 'executive_team_list.html', {'members': members})

@admin_required
def executive_team_create(request):
    if request.method == 'POST':
        form = ExecutiveTeamMemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Executive team member added successfully.')
            return redirect('executive_team_list')
    else:
        form = ExecutiveTeamMemberForm()
    return render(request, 'executive_team_create.html', {'form': form})


@admin_required
def approve_account_application(request, application_id):
    application = get_object_or_404(AccountApplication, pk=application_id)

    if application.is_approved:
        messages.warning(request, "This application has already been approved.")
        return redirect('account_application_list')

    if User.objects.filter(email=application.email).exists():
        messages.error(request, "A user with this email already exists.")
        return redirect('account_application_list')

    # Generate random password
    password = get_random_string(10)

    # Create user
    user = User.objects.create_user(
        username=application.email,
        email=application.email,
        full_name=f"{application.full_first_name} {application.full_surname}",
        phone_number=application.mobile_phone_1,
        role=User.Role.BASIC_USER,
        is_approved=True,
    )
    user.set_password(password)
    user.save()

    # Link application to the new user
    application.user = user
    application.is_approved = True
    application.save()

    # Prepare email content
    html_content = (
        f"<p>Hi {application.full_first_name},</p>"
        f"<p>Your alumni account has been created.</p>"
        f"<ul>"
        f"<li><strong>Email:</strong> {application.email}</li>"
        f"<li><strong>Password:</strong> {password}</li>"
        f"</ul>"
        f"<p>Please log in and change your password.</p>"
        f"<p>Welcome aboard!</p>"
    )
    
    # Create SendGrid email with compatible initialization
    email_message = Mail(
        from_email=settings.DEFAULT_FROM_EMAIL,
        to_emails=[application.email],
        subject="Your Alumni Account Has Been Approved",
        html_content=html_content
    )

    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY) 
        response = sg.send(email_message)
        print(f"SendGrid response: {response.status_code}, {response.body}, {response.headers}")
        if response.status_code not in [200, 202]:
            raise Exception(f"SendGrid responded with status code {response.status_code}")
        messages.success(request, f"Account for {application.full_first_name} has been created and approved.")
    except Exception as e:
        print(f"Error sending email: {e}")
        messages.error(request, f"Account created, but failed to send email: {e}")

    return redirect('account_application_list')

