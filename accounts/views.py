from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import login, logout, get_user_model
from .forms import CustomUserCreationForm, AccountApplicationForm
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm


# views.py

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # You can uncomment the login line if you want to log the user in immediately
            # login(request, user)
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('https://www.thenazarenejonahsalumni.com/login')
        else:
            # If form is invalid, we'll handle the errors in the template
            pass
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def account_application_success(request):
    return render(request, 'registration/signup_success.html')

def apply_account(request):
    if request.method == 'POST':
        form = AccountApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AccountApplicationForm()
    return render(request, 'apply_account.html', {'form': form})



def account_application_create(request):
    if request.method == 'POST':
        form = AccountApplicationForm(request.POST)
        
        if form.is_valid():
            try:
                app = form.save(commit=False)
                
                # Process the form data before saving
                app.is_approved = False  # Default to not approved
                
                # Handle the classes_attended field (already processed in form clean)
                # Handle UCE/UACE fields (already processed in form clean)
                
                app.save()
                
                # Send emails only if in production or if email is configured
                if settings.SENDGRID_API_KEY:
                    sg = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)

                    # Admin notification email
                    admin_email = Mail(
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to_emails=settings.ADMIN_EMAIL,
                        subject=f'New Alumni Application: {app.full_first_name} {app.full_surname}',
                        html_content=(
                            f'<h3>New Alumni Application Received</h3>'
                            f'<p><strong>Name:</strong> {app.full_first_name} {app.full_surname}</p>'
                            f'<p><strong>Email:</strong> {app.email}</p>'
                            f'<p><strong>Phone:</strong> {app.mobile_phone_1}</p>'
                            f'<p><strong>Years at Nazarene:</strong> {app.year_joined_jonahs}-{app.year_left_jonahs}</p>'
                            f'<p><strong>House:</strong> {app.house}</p>'
                            f'<p><strong>Classes Attended:</strong> {app.classes_attended}</p>'
                            f'<p><strong>Application Date:</strong> {app.created_at.strftime("%Y-%m-%d %H:%M")}</p>'
                            f'<p>Please review this application in the admin panel.</p>'
                        )
                    )
                    sg.send(admin_email)

                    # Applicant confirmation email
                    applicant_email = Mail(
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to_emails=app.email,
                        subject='Your Nazarene Alumni Application Has Been Received',
                        html_content=(
                            f'<h3>Dear {app.full_first_name},</h3>'
                            f'<p>Thank you for submitting your application to The Nazarene Alumni Association. '
                            f'We have received your application and will review it shortly.</p>'
                            f'<p>You will be contacted once your application has been processed. This typically takes '
                            f'3-5 business days.</p>'
                            f'<h4>Application Summary</h4>'
                            f'<ul>'
                            f'<li><strong>Name:</strong> {app.full_first_name} {app.full_surname}</li>'
                            f'<li><strong>Application Date:</strong> {app.created_at.strftime("%Y-%m-%d %H:%M")}</li>'
                            f'<li><strong>Reference ID:</strong> NA-{app.id:04d}</li>'
                            f'</ul>'
                            f'<p>If you have any questions, please reply to this email.</p>'
                            f'<p>Best regards,<br>The Nazarene Alumni Association</p>'
                        )
                    )
                    sg.send(applicant_email)

                messages.success(request, 
                    "Application submitted successfully! You will receive a confirmation email shortly.")
                return redirect('signup')

            except Exception as e:
                # Log the error for debugging
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Error processing application: {str(e)}", exc_info=True)
                
                # Still save the application but notify admin of email failure
                if 'app' in locals():
                    app.save()
                
                messages.warning(request, 
                    "Your application has been received, but there was an issue with email notifications. "
                    "We will contact you soon.")
                return redirect('signup')
        else:
            # Form has validation errors
            messages.error(request, 
                "Please correct the errors below and try again. If problems persist, contact support.")
            # Log form errors for debugging
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Form validation errors: {form.errors}")
    else:
        form = AccountApplicationForm()

    return render(request, 'application_form.html', {'form': form})


def account_application_success(request):
    return render(request, 'application_success.html')

