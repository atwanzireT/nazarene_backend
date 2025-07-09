from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import AccountApplication

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        required=True,
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'appearance-none block w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg placeholder-gray-400 text-gray-900 dark:text-white bg-white dark:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 transition-colors duration-200',
            'placeholder': 'Your username'
        })
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'appearance-none block w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg placeholder-gray-400 text-gray-900 dark:text-white bg-white dark:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 transition-colors duration-200',
            'placeholder': 'email@example.com'
        })
    )
    
    phone_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'appearance-none block w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg placeholder-gray-400 text-gray-900 dark:text-white bg-white dark:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 transition-colors duration-200',
            'placeholder': '+1 (555) 123-4567'
        })
    )
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'appearance-none block w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg placeholder-gray-400 text-gray-900 dark:text-white bg-white dark:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 transition-colors duration-200',
            'placeholder': 'Create a strong password'
        })
    )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'appearance-none block w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg placeholder-gray-400 text-gray-900 dark:text-white bg-white dark:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 transition-colors duration-200',
            'placeholder': 'Confirm your password'
        })
    )

    class Meta:
        model = User
        fields = ("username", "email", "phone_number", "password1", "password2")




from django import forms
from .models import AccountApplication, ClassLevel
from phonenumber_field.formfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class AccountApplicationForm(forms.ModelForm):
    # Personal Details
    full_first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-150',
            'placeholder': 'John'
        }),
        required=True,
        help_text="Your legal first name as it appears on official documents."
    )
    
    full_surname = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-150',
            'placeholder': 'Doe'
        }),
        required=True,
        help_text="Your family name or surname."
    )
    
    other_names = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-150',
            'placeholder': 'Nickname or other names'
        }),
        required=False,
        help_text="Any other names you're commonly known by."
    )
    
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-150',
            'type': 'date'
        }),
        required=True,
        help_text="Format: DD/MM/YYYY"
    )
    
    gender = forms.ChoiceField(
        choices=AccountApplication.gender_choices,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-150'
        }),
        required=True
    )
    
    nationality = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-150',
            'placeholder': 'Ugandan'
        }),
        required=True
    )
    
    # Contact Details
    mobile_phone_1 = PhoneNumberField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-150',
            'placeholder': '+256...'
        }),
        required=True,
        help_text="Primary contact number in international format."
    )
    
    mobile_phone_2 = PhoneNumberField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-150',
            'placeholder': '+256...'
        }),
        required=False,
        help_text="Optional secondary contact number."
    )
    
    home_phone_1 = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-150',
            'placeholder': '0414234567'
        }),
        required=False,
        max_length=15,
        help_text="Landline number if applicable."
    )
    
    home_phone_2 = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-150',
            'placeholder': 'Additional landline'
        }),
        required=False,
        max_length=15
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-150',
            'placeholder': 'your.email@example.com'
        }),
        required=True,
        help_text="We'll send important communications to this address."
    )
    
    current_location = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-150',
            'placeholder': 'Kampala, Uganda'
        }),
        required=True,
        help_text="Your current city and country of residence."
    )
    
    permanent_home_address = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-150',
            'placeholder': 'Full permanent address including district',
            'rows': 3
        }),
        required=True,
        help_text="Your permanent home address for official records."
    )
    
    # Academic Details
    year_joined_jonahs = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-150',
            'placeholder': 'e.g. 2005'
        }),
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(timezone.now().year)
        ],
        required=True,
        help_text="The year you first joined Jonah's Academy."
    )
    
    house = forms.ChoiceField(
        choices=AccountApplication._meta.get_field('house').choices,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-150'
        }),
        required=True,
        help_text="Which house did you belong to during your time at Jonah's?"
    )
    
    classes_attended = forms.ModelMultipleChoiceField(
        queryset=ClassLevel.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'rounded text-blue-600 focus:ring-blue-500 border-gray-300'
        }),
        required=True,
        help_text="Select all classes you attended at Jonah's Academy."
    )
    
    year_left_jonahs = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-150',
            'placeholder': 'e.g. 2011'
        }),
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(timezone.now().year)
        ],
        required=True,
        help_text="The year you completed or left Jonah's Academy."
    )
    
    sat_uce = forms.ChoiceField(
        choices=AccountApplication._meta.get_field('sat_uce').choices,
        widget=forms.RadioSelect(attrs={
            'class': 'text-blue-600 focus:ring-blue-500 border-gray-300'
        }),
        required=True,
        initial="NO",
        help_text="Did you sit for Uganda Certificate of Education (UCE) exams?"
    )
    
    sat_uace = forms.ChoiceField(
        choices=AccountApplication._meta.get_field('sat_uace').choices,
        widget=forms.RadioSelect(attrs={
            'class': 'text-blue-600 focus:ring-blue-500 border-gray-300'
        }),
        required=True,
        initial="NO",
        help_text="Did you sit for Uganda Advanced Certificate of Education (UACE) exams?"
    )
    
    uce_class_year = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-150',
            'placeholder': 'e.g. 2010'
        }),
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(timezone.now().year)
        ],
        required=False,
        help_text="If you sat for UCE, which year was it?"
    )
    
    uace_class_year = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-150',
            'placeholder': 'e.g. 2012'
        }),
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(timezone.now().year)
        ],
        required=False,
        help_text="If you sat for UACE, which year was it?"
    )
    
    # Association Interests
    association_interests = forms.MultipleChoiceField(
        choices=[
            ('mentorship_career_guidance', 'Mentorship & Career Guidance'),
            ('skill_sharing', 'Skill Sharing'),
            ('networking', 'Networking'),
            ('fundraisers', 'Fundraisers'),
            ('event_planning', 'Event Planning'),
            ('cohort_mobilisation', 'Cohort Mobilisation'),
            ('volunteering', 'Volunteering'),
        ],
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'rounded text-blue-600 focus:ring-blue-500 border-gray-300'
        }),
        required=False,
        help_text="Select areas you're interested in participating in (select all that apply)"
    )
    
    # Areas of Contribution
    contribution_areas = forms.MultipleChoiceField(
        choices=[
            ('financial_support', 'Financial Support'),
            ('charitable_outreach_programs', 'Charitable Outreach Programs'),
            ('alumni_sports_league', 'Alumni Sports League'),
            ('alumni_dinner', 'Alumni Dinner'),
            ('events_at_school', 'Events at School'),
            ('all_get_together_events', 'All Get-Together Events'),
        ],
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'rounded text-blue-600 focus:ring-blue-500 border-gray-300'
        }),
        required=False,
        help_text="Select areas you might be able to contribute to (select all that apply)"
    )
    
    # Consent
    consent_given = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
            'class': 'rounded text-blue-600 focus:ring-blue-500 border-gray-300'
        }),
        required=True,
        label="I consent to the processing of my personal data for alumni association purposes."
    )

    class Meta:
        model = AccountApplication
        exclude = ['user', 'is_approved', 'created_at', 'updated_at']
        error_messages = {
            'email': {
                'unique': "This email address is already registered. Please use a different email or contact support if this is yours."
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set initial values for checkbox groups
        self.fields['association_interests'].initial = [
            field for field in [
                'mentorship_career_guidance',
                'skill_sharing',
                'networking',
                'fundraisers',
                'event_planning',
                'cohort_mobilisation',
                'volunteering'
            ] if self.instance.pk and getattr(self.instance, field)
        ]
        
        self.fields['contribution_areas'].initial = [
            field for field in [
                'financial_support',
                'charitable_outreach_programs',
                'alumni_sports_league',
                'alumni_dinner',
                'events_at_school',
                'all_get_together_events'
            ] if self.instance.pk and getattr(self.instance, field)
        ]

    def clean(self):
        cleaned_data = super().clean()
        
        # Validate year_left is after year_joined
        year_joined = cleaned_data.get('year_joined_jonahs')
        year_left = cleaned_data.get('year_left_jonahs')
        
        if year_joined and year_left and year_left < year_joined:
            self.add_error('year_left_jonahs', "Year left must be after year joined")
        
        # Validate UCE/UACE years if selected
        sat_uce = cleaned_data.get('sat_uce')
        uce_year = cleaned_data.get('uce_class_year')
        
        if sat_uce == "YES" and not uce_year:
            self.add_error('uce_class_year', "Please specify the year you sat for UCE")
        
        sat_uace = cleaned_data.get('sat_uace')
        uace_year = cleaned_data.get('uace_class_year')
        
        if sat_uace == "YES" and not uace_year:
            self.add_error('uace_class_year', "Please specify the year you sat for UACE")
        
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Save checkbox group values to individual fields
        for field in [
            'mentorship_career_guidance',
            'skill_sharing',
            'networking',
            'fundraisers',
            'event_planning',
            'cohort_mobilisation',
            'volunteering'
        ]:
            setattr(instance, field, field in self.cleaned_data.get('association_interests', []))
        
        for field in [
            'financial_support',
            'charitable_outreach_programs',
            'alumni_sports_league',
            'alumni_dinner',
            'events_at_school',
            'all_get_together_events'
        ]:
            setattr(instance, field, field in self.cleaned_data.get('contribution_areas', []))
        
        if commit:
            instance.save()
            self.save_m2m()
        
        return instance