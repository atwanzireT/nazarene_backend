from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import * 
from .models import AccountApplication
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class EmailLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
            'autofocus': True
        })
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
    )

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


class ExecutiveTeamMemberForm(forms.ModelForm):
    class Meta:
        model = ExecutiveTeamMember
        fields = [
            'position', 'name', 'email', 'phone',
            'term_start', 'term_end', 'image_url',
            'rank', 'active'
        ]
        widgets = {
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'term_start': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'term_end': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'image_url': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'rank': forms.NumberInput(attrs={'class': 'form-control'}),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ProjectImageForm(forms.ModelForm):
    class Meta:
        model = ProjectImage
        fields = ['image', 'caption']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'caption': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
        
class EventImageForm(forms.ModelForm):
    class Meta:
        model = EventImage
        fields = ['image', 'caption']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'caption': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
        
class ActivityImageForm(forms.ModelForm):
    class Meta:
        model = ActivityImage
        fields = ['image', 'caption']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'caption': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
        
        
class AccountApplicationForm(forms.ModelForm):
    # Override classes_attended to handle multiple checkboxes
    classes_attended = forms.MultipleChoiceField(
        choices=[
            ('S1', 'S1'),
            ('S2', 'S2'),
            ('S3', 'S3'),
            ('S4', 'S4'),
            ('S5', 'S5'),
            ('S6', 'S6'),
        ],
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=True,
        error_messages={'required': 'Please select at least one class attended.'}
    )
    
    # Override sat_uce and sat_uace to handle boolean values properly
    sat_uce = forms.ChoiceField(
        choices=[('', ''), ('yes', 'Yes'), ('no', 'No')],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        required=False
    )
    
    sat_uace = forms.ChoiceField(
        choices=[('', ''), ('yes', 'Yes'), ('no', 'No')],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        required=False
    )

    class Meta:
        model = AccountApplication
        fields = '__all__'
        exclude = ['user', 'created_at', 'updated_at']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add Bootstrap classes to form fields
        for field_name, field in self.fields.items():
            if field_name in ['classes_attended', 'sat_uce', 'sat_uace']:
                continue  # These are handled above
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            else:
                field.widget.attrs.update({'class': 'form-control'})
                
        # Make house field required with proper validation
        self.fields['house'].required = True
        self.fields['house'].empty_label = None  # Remove empty option
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Handle classes_attended - convert list to comma-separated string
        classes_attended = cleaned_data.get('classes_attended')
        if classes_attended:
            if isinstance(classes_attended, list):
                cleaned_data['classes_attended'] = ','.join(classes_attended)
        else:
            raise forms.ValidationError("Please select at least one class attended.")
        
        # Handle UCE/UACE validation
        sat_uce = cleaned_data.get('sat_uce')
        sat_uace = cleaned_data.get('sat_uace')
        uce_class_year = cleaned_data.get('uce_class_year')
        uace_class_year = cleaned_data.get('uace_class_year')
        
        # Convert 'yes'/'no' strings to boolean for model
        if sat_uce == 'yes':
            cleaned_data['sat_uce'] = True
        elif sat_uce == 'no':
            cleaned_data['sat_uce'] = False
        else:
            cleaned_data['sat_uce'] = None
            
        if sat_uace == 'yes':
            cleaned_data['sat_uace'] = True
        elif sat_uace == 'no':
            cleaned_data['sat_uace'] = False
        else:
            cleaned_data['sat_uace'] = None
        
        # Validate UCE/UACE year requirements
        if cleaned_data.get('sat_uce') is True and not uce_class_year:
            raise forms.ValidationError("UCE class year is required if you sat UCE.")
        if cleaned_data.get('sat_uace') is True and not uace_class_year:
            raise forms.ValidationError("UACE class year is required if you sat UACE.")
            
        return cleaned_data