from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

# Custom User Model
class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', _('Admin')
        STAFF = 'STAFF', _('Staff')
        BASIC_USER = 'BASIC_USER', _('Basic_user')

    email = models.EmailField(_('email_address'), unique=True, blank=False)
    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.BASIC_USER,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = "custom_user"
        db_table_comment = "Custom user model using email for authentication with role-based access"

    def __str__(self):
        return f"{self.email} - {self.role}"

# Account Application
class AccountApplication(models.Model):
    # Personal Details
    full_first_name = models.CharField(max_length=100)
    full_middle_name = models.CharField(max_length=100, blank=True, null=True)
    full_surname = models.CharField(max_length=100)
    other_names = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField()
    gender_choices = [('Male', 'Male'), ('Female', 'Female')]
    gender = models.CharField(max_length=10, choices=gender_choices)
    nationality = models.CharField(max_length=50)

    # Contact Details
    mobile_phone_1 = models.CharField(max_length=15)
    mobile_phone_2 = models.CharField(max_length=15, blank=True, null=True)
    home_phone_1 = models.CharField(max_length=15, blank=True, null=True)
    home_phone_2 = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)
    current_location = models.CharField(max_length=255)
    permanent_home_address = models.CharField(max_length=255)

    # Academic Details
    year_joined_jonahs = models.PositiveIntegerField()
    house = models.CharField(max_length=100)
    classes_attended = models.CharField(max_length=255)
    year_left_jonahs = models.PositiveIntegerField()
    sat_uce = models.BooleanField(default=False)
    sat_uace = models.BooleanField(default=False)
    uce_class_year = models.PositiveIntegerField(blank=True, null=True)
    uace_class_year = models.PositiveIntegerField(blank=True, null=True)

    # Association Interests
    mentorship_career_guidance = models.BooleanField(default=False)
    skill_sharing = models.BooleanField(default=False)
    networking = models.BooleanField(default=False)
    fundraisers = models.BooleanField(default=False)
    event_planning = models.BooleanField(default=False)
    cohort_mobilisation = models.BooleanField(default=False)
    volunteering = models.BooleanField(default=False)

    # Areas of Contribution
    financial_support = models.BooleanField(default=False)
    charitable_outreach_programs = models.BooleanField(default=False)
    alumni_sports_league = models.BooleanField(default=False)
    alumni_dinner = models.BooleanField(default=False)
    events_at_school = models.BooleanField(default=False)
    all_get_together_events = models.BooleanField(default=False)

    # Consent
    consent_given = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_first_name} {self.full_surname} - {self.email}"

# Project & Activity
class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('ongoing', 'Ongoing'), ('completed', 'Completed')])
    progress = models.PositiveIntegerField(default=0)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    cover_image = models.ImageField(upload_to='event_covers/', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False, null=True, blank=True )

    def __str__(self):
        return self.title

class Activity(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='activities')
    title = models.CharField(max_length=200)
    description = models.TextField()
    activity_date = models.DateField()
    cover_image = models.ImageField(upload_to='event_covers/', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True,  editable=False, null=True, blank=True)

    def __str__(self):
        return f"{self.project.title} - {self.title}"

# Events
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_date = models.DateTimeField()
    location = models.CharField(max_length=200)
    slots = models.PositiveIntegerField(null=True, blank=True)
    cover_image = models.ImageField(upload_to='event_covers/', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False, null=True, blank=True)

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


# User Activity
class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.CharField(max_length=50)  # e.g., "login" or "logout"
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.activity} at {self.timestamp}"