from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.utils.timesince import timesince
from django.utils import timezone
from datetime import date
from .models import *

# -------------------
# USER
# -------------------

class UserSerializer(serializers.ModelSerializer):
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'full_name', 'email', 'phone_number',
            'is_approved', 'role', 'role_display', 'date_joined'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'role': {'read_only': True},
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError(_("A user with this email already exists."))
        return value


# -------------------
# ACCOUNT APPLICATION
# -------------------

class AccountApplicationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    full_name = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()

    class Meta:
        model = AccountApplication
        exclude = ['created_at', 'updated_at']
        read_only_fields = ['is_approved']
        extra_kwargs = {
            'email': {'validators': []},
            'consent_given': {
                'required': True,
                'error_messages': {
                    'required': _('You must give consent to proceed.')
                }
            }
        }

    def get_full_name(self, obj):
        names = [obj.full_first_name, obj.full_middle_name, obj.full_surname]
        return " ".join(filter(None, names))

    def get_age(self, obj):
        today = date.today()
        return today.year - obj.date_of_birth.year - (
            (today.month, today.day) < (obj.date_of_birth.month, obj.date_of_birth.day)
        )

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_("This email is already registered."))
        if AccountApplication.objects.filter(email=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError(_("An application with this email already exists."))
        return value

    def validate(self, data):
        if data.get('year_left_jonahs') < data.get('year_joined_jonahs'):
            raise serializers.ValidationError({'year_left_jonahs': _("Year left cannot be before year joined.")})
        if data.get('sat_uce') and not data.get('uce_class_year'):
            raise serializers.ValidationError({'uce_class_year': _("Please provide the year you sat for UCE.")})
        if data.get('sat_uace') and not data.get('uace_class_year'):
            raise serializers.ValidationError({'uace_class_year': _("Please provide the year you sat for UACE.")})
        if not data.get('consent_given'):
            raise serializers.ValidationError({'consent_given': _("You must give consent to proceed.")})
        return data


# -------------------
# PROJECTS & ACTIVITIES
# -------------------

class ActivitySerializer(serializers.ModelSerializer):
    project_title = serializers.CharField(source='project.title', read_only=True)

    class Meta:
        model = Activity
        fields = [
            'id', 'title', 'description', 'activity_date',
            'project', 'project_title', 'location', 'status',
            'cover_image', 'created'
        ]
        read_only_fields = ['created']

    def validate_activity_date(self, value):
        project_id = self.initial_data.get('project')
        if project_id:
            project = Project.objects.get(pk=project_id)
            if value < project.start_date:
                raise serializers.ValidationError(_("Activity date cannot be before project start date."))
            if project.end_date and value > project.end_date:
                raise serializers.ValidationError(_("Activity date cannot be after project end date."))
        return value


class ProjectSerializer(serializers.ModelSerializer):
    activities = ActivitySerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    duration = serializers.SerializerMethodField()
    is_active = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description', 'status', 'status_display',
            'progress', 'start_date', 'end_date', 'budget', 'raised_amount',
            'location', 'cover_image', 'is_featured', 'activities',
            'duration', 'is_active', 'created'
        ]
        read_only_fields = ['created']

    def get_duration(self, obj):
        return (obj.end_date - obj.start_date).days if obj.end_date else None

    def get_is_active(self, obj):
        today = timezone.now().date()
        return obj.start_date <= today and (obj.end_date is None or obj.end_date >= today)

    def validate(self, data):
        if data.get('end_date') and data['end_date'] < data['start_date']:
            raise serializers.ValidationError({'end_date': _("End date cannot be before start date.")})
        if data.get('progress') and not (0 <= data['progress'] <= 100):
            raise serializers.ValidationError({'progress': _("Progress must be between 0 and 100.")})
        return data


class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ['id', 'project', 'image', 'caption', 'uploaded_at']


class ActivityImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityImage
        fields = ['id', 'activity', 'image', 'caption', 'uploaded_at']


# -------------------
# EVENTS & REGISTRATION
# -------------------

class EventSerializer(serializers.ModelSerializer):
    available_slots = serializers.SerializerMethodField()
    is_past = serializers.SerializerMethodField()
    registered_count = serializers.SerializerMethodField()
    is_registered = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'event_date', 'location', 'slots', 'status',
            'organizer', 'contact_email', 'contact_phone', 'is_open',
            'cover_image', 'available_slots', 'registered_count',
            'is_past', 'is_registered', 'created'
        ]
        read_only_fields = ['created']

    def get_available_slots(self, obj):
        if obj.slots is None:
            return None
        return max(0, obj.slots - EventRegistration.objects.filter(event=obj).count())

    def get_is_past(self, obj):
        return obj.event_date < timezone.now()

    def get_registered_count(self, obj):
        return EventRegistration.objects.filter(event=obj).count()

    def get_is_registered(self, obj):
        user = self.context.get('request').user
        return user.is_authenticated and EventRegistration.objects.filter(event=obj, user=user).exists()


class EventRegistrationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    event_title = serializers.CharField(source='event.title', read_only=True)
    event_date = serializers.DateTimeField(source='event.event_date', read_only=True)

    class Meta:
        model = EventRegistration
        fields = ['id', 'user', 'event', 'event_title', 'event_date', 'registered_at']
        read_only_fields = ['registered_at']

    def validate(self, data):
        event = data['event']
        user = self.context['request'].user
        if EventRegistration.objects.filter(event=event, user=user).exists():
            raise serializers.ValidationError(_("You are already registered for this event."))
        if event.slots and EventRegistration.objects.filter(event=event).count() >= event.slots:
            raise serializers.ValidationError(_("This event is already full."))
        if event.event_date < timezone.now():
            raise serializers.ValidationError(_("Cannot register for past events."))
        return data


class EventImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventImage
        fields = ['id', 'event', 'image', 'caption', 'uploaded_at']


# -------------------
# NOTIFICATIONS
# -------------------

class NotificationSerializer(serializers.ModelSerializer):
    time_since = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'is_read', 'created_at', 'time_since']
        read_only_fields = ['created_at']

    def get_time_since(self, obj):
        return timesince(obj.created_at, timezone.now())


class ExecutiveTeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExecutiveTeamMember
        fields = '__all__'


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = '__all__'


