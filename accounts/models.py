from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
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
        default=Role.ADMIN,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = "custom_user"
        db_table_comment = "Custom user model using email for authentication with role-based access"

    def __str__(self):
        return f"{self.email} - {self.role}"


class ClassLevel(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "class_level"
        db_table_comment = "Model representing different class levels in the school"

    def __str__(self):
        return self.name
    
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
    full_surname = models.CharField(max_length=100)
    other_names = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField()
    gender_choices = [('Male', 'Male'), ('Female', 'Female')]
    gender = models.CharField(max_length=10, choices=gender_choices)
    nationality = models.CharField(max_length=50)

    # Contact Details
    mobile_phone_1 = PhoneNumberField()
    mobile_phone_2 = PhoneNumberField(blank=True, null =True)
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
    
    classes_attended = models.ManyToManyField(
        ClassLevel,
        related_name='account_applications',
        help_text="Select the classes attended during your time at Jonah's Academy."
    )
    year_left_jonahs = models.PositiveIntegerField()
    sat_uce = models.CharField(
        max_length=10,
        choices=[
            ("YES", "Yes"),
            ("NO", "No"),
        ],
        default="NO"
    )
    sat_uace = models.CharField(
        max_length=10,
        choices=[
            ("YES", "Yes"),
            ("NO", "No"),
        ],
        default="NO"
    )
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
  