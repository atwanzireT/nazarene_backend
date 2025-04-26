from rest_framework import serializers
from .models import (
    User,
    AccountApplication,
    Project,
    Activity,
    Event,
    EventRegistration,
    Notification
)
from django.utils.translation import gettext_lazy as _

class UserSerializer(serializers.ModelSerializer):
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 
            'username', 
            'full_name', 
            'email', 
            'phone_number', 
            'is_approved',
            'role',
            'role_display',
            'date_joined'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'role': {'read_only': True},  # Typically role should be managed separately
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError(_("A user with this email already exists."))
        return value


class ActivitySerializer(serializers.ModelSerializer):
    project_title = serializers.CharField(source='project.title', read_only=True)
    
    class Meta:
        model = Activity
        fields = [
            'id', 
            'title', 
            'description', 
            'activity_date', 
            'project', 
            'project_title',
            'cover_image',
            'created'
        ]
        read_only_fields = ['created']

    def validate_activity_date(self, value):
        project = self.initial_data.get('project')
        if project:
            project = Project.objects.get(pk=project)
            if value < project.start_date:
                raise serializers.ValidationError(
                    _("Activity date cannot be before project start date.")
                )
            if project.end_date and value > project.end_date:
                raise serializers.ValidationError(
                    _("Activity date cannot be after project end date.")
                )
        return value


class ProjectSerializer(serializers.ModelSerializer):
    activities = ActivitySerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    duration = serializers.SerializerMethodField()
    is_active = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 
            'title', 
            'description', 
            'status',
            'status_display',
            'progress', 
            'start_date', 
            'end_date', 
            'cover_image',
            'activities',
            'duration',
            'is_active',
            'created'
        ]
        read_only_fields = ['created']

    def get_duration(self, obj):
        if obj.end_date:
            return (obj.end_date - obj.start_date).days
        return None

    def get_is_active(self, obj):
        from django.utils import timezone
        today = timezone.now().date()
        return obj.start_date <= today and (obj.end_date is None or obj.end_date >= today)

    def validate(self, data):
        if data.get('end_date') and data['end_date'] < data['start_date']:
            raise serializers.ValidationError({
                'end_date': _("End date cannot be before start date.")
            })
        if data.get('progress') and (data['progress'] < 0 or data['progress'] > 100):
            raise serializers.ValidationError({
                'progress': _("Progress must be between 0 and 100.")
            })
        return data


class EventSerializer(serializers.ModelSerializer):
    available_slots = serializers.SerializerMethodField()
    is_past = serializers.SerializerMethodField()
    registered_count = serializers.SerializerMethodField()
    is_registered = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'id', 
            'title', 
            'description', 
            'event_date', 
            'location', 
            'slots',
            'available_slots',
            'registered_count',
            'is_past',
            'is_registered',
            'cover_image',
            'created'
        ]
        read_only_fields = ['created']

    def get_available_slots(self, obj):
        if obj.slots is None:
            return None
        registered = EventRegistration.objects.filter(event=obj).count()
        return max(0, obj.slots - registered)

    def get_is_past(self, obj):
        from django.utils import timezone
        return obj.event_date < timezone.now()

    def get_registered_count(self, obj):
        return EventRegistration.objects.filter(event=obj).count()

    def get_is_registered(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return EventRegistration.objects.filter(
                event=obj, 
                user=request.user
            ).exists()
        return False


class EventRegistrationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    event_title = serializers.CharField(source='event.title', read_only=True)
    event_date = serializers.DateTimeField(source='event.event_date', read_only=True)

    class Meta:
        model = EventRegistration
        fields = [
            'id', 
            'user', 
            'event', 
            'event_title',
            'event_date',
            'registered_at'
        ]
        read_only_fields = ['registered_at']

    def validate(self, data):
        event = data['event']
        user = self.context['request'].user
        
        # Check if already registered
        if EventRegistration.objects.filter(event=event, user=user).exists():
            raise serializers.ValidationError(_("You are already registered for this event."))
        
        # Check if event has available slots
        if event.slots is not None:
            registered = EventRegistration.objects.filter(event=event).count()
            if registered >= event.slots:
                raise serializers.ValidationError(_("This event is already full."))
        
        # Check if event is in the past
        from django.utils import timezone
        if event.event_date < timezone.now():
            raise serializers.ValidationError(_("Cannot register for past events."))
        
        return data


class NotificationSerializer(serializers.ModelSerializer):
    time_since = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            'id', 
            'title', 
            'message', 
            'is_read', 
            'created_at',
            'time_since'
        ]
        read_only_fields = ['created_at']

    def get_time_since(self, obj):
        from django.utils import timezone
        from django.utils.timesince import timesince
        return timesince(obj.created_at, timezone.now())


class AccountApplicationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    full_name = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()

    class Meta:
        model = AccountApplication
        exclude = ['created_at', 'updated_at']
        read_only_fields = ['is_approved']
        extra_kwargs = {
            'email': {
                'validators': []  # We'll handle validation in validate_email
            },
            'consent_given': {
                'required': True,
                'error_messages': {
                    'required': _('You must give consent to proceed.')
                }
            }
        }

    def get_full_name(self, obj):
        return f"{obj.full_first_name} {obj.full_surname}"

    def get_age(self, obj):
        from datetime import date
        today = date.today()
        return today.year - obj.date_of_birth.year - (
            (today.month, today.day) < (obj.date_of_birth.month, obj.date_of_birth.day)
        )

    def validate_email(self, value):
        """
        Check that the email isn't already used by a user or in another application.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_("This email is already registered."))
        
        if AccountApplication.objects.filter(email=value).exclude(
            pk=self.instance.pk if self.instance else None
        ).exists():
            raise serializers.ValidationError(_("An application with this email already exists."))
        
        return value

    def validate(self, data):
        """
        Add additional validation for the application.
        """
        if data.get('year_left_jonahs') < data.get('year_joined_jonahs'):
            raise serializers.ValidationError({
                'year_left_jonahs': _("Year left cannot be before year joined.")
            })
        
        if data.get('sat_uce') and not data.get('uce_class_year'):
            raise serializers.ValidationError({
                'uce_class_year': _("Please provide the year you sat for UCE.")
            })
            
        if data.get('sat_uace') and not data.get('uace_class_year'):
            raise serializers.ValidationError({
                'uace_class_year': _("Please provide the year you sat for UACE.")
            })
        
        if not data.get('consent_given'):
            raise serializers.ValidationError({
                'consent_given': _("You must give consent to proceed.")
            })
        
        return data