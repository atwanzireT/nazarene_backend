from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

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
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='account_application',
        null=True,
        blank=True
    )
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
    house = models.CharField(
        max_length=100,
        choices=[
            ("ST. BALIKUDDEMBE HOUSE", "ST. BALIKUDDEMBE HOUSE"),
            ("ST. JOHNMARY HOUSE", "ST. JOHNMARY HOUSE"),
            ("ST. KIZITO HOUSE", "ST. KIZITO HOUSE"),
            ("ST. CHARLES HOUSE", "ST. CHARLES HOUSE"),
            ("FORGOT/DIDN'T HAVE HOUSE", "FORGOT/DIDN'T HAVE HOUSE"),
        ]
    )
    
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
    
# -------------------------
# Projects and Activities
# -------------------------

class Project(models.Model):
    STATUS_CHOICES = (
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('postponed', 'Postponed'),
        ('archived', 'Archived'),
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    progress = models.PositiveIntegerField(default=0)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    budget = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    raised_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    location = models.CharField(max_length=200, null=True, blank=True)
    cover_image = models.ImageField(upload_to='project_covers/', null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, editable=False, null=True, blank=True)

    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='project_gallery/')
    caption = models.CharField(max_length=200, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.project.title} - {self.caption or 'No Caption'}"


class Activity(models.Model):
    STATUS_CHOICES = (
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('postponed', 'Postponed'),
        ('archived', 'Archived'),
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='activities')
    title = models.CharField(max_length=200)
    description = models.TextField()
    activity_date = models.DateField()
    location = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default = "upcoming")
    cover_image = models.ImageField(upload_to='activity_covers/', null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False, null=True, blank=True)

    def __str__(self):
        return f"{self.project.title} - {self.title}"


class ActivityImage(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='activity_gallery/')
    caption = models.CharField(max_length=200, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.activity.title} - {self.caption or 'No Caption'}"


# -------------------------
# Events and Registration
# -------------------------

class Event(models.Model):
    STATUS_CHOICES = (
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('postponed', 'Postponed'),
        ('archived', 'Archived'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_date = models.DateTimeField()
    location = models.CharField(max_length=200)
    slots = models.PositiveIntegerField(null=True, blank=True)
    organizer = models.CharField(max_length=100, null=True, blank=True)
    contact_email = models.EmailField(null=True, blank=True)
    contact_phone = models.CharField(max_length=20, null=True, blank=True)
    is_open = models.BooleanField(default=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default = "upcoming")
    cover_image = models.ImageField(upload_to='event_covers/', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False, null=True, blank=True)

    def __str__(self):
        return self.title


class EventImage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='event_gallery/')
    caption = models.CharField(max_length=200, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.event.title} - {self.caption or 'No Caption'}"


class EventRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')
        verbose_name = "Event Registration"
        verbose_name_plural = "Event Registrations"

    def __str__(self):
        return f"{self.user.username} registered for {self.event.title}"
        
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
    activity = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.activity} at {self.timestamp}"


class ExecutiveTeamMember(models.Model):
    position = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    term_start = models.DateField()
    term_end = models.DateField()
    image_url = models.ImageField(upload_to="staff", default='placeholder.jpg')
    rank = models.PositiveIntegerField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.position}"

    class Meta:
        ordering = ['rank']



class ContactMessage(models.Model):
    CATEGORY_CHOICES = [
        ('general', 'General Inquiry'),
        ('alumni', 'Alumni Support'),
        ('events', 'Events & Programming'),
        ('donations', 'Donations & Giving'),
        ('careers', 'Career Services'),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255, blank=True)
    message = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject or 'No Subject'}"


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('birthday', 'Birthday'),
        ('event', 'Event'),
        ('project', 'Project'),
        ('activity', 'Activity'),
        ('general', 'General'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    message = models.TextField()
    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='general')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
