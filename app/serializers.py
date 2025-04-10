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

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'email', 'phone_number', 'is_approved']

# Account Application Serializer
class AccountApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountApplication
        fields = [
            'id', 'full_name', 'email', 'phone_number',
            'course', 'year_of_graduation', 'message',
            'is_reviewed', 'is_approved', 'applied_at'
        ]
        read_only_fields = ['is_reviewed', 'is_approved', 'applied_at']

# Activity Serializer
class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'title', 'description', 'activity_date', 'project']

# Project Serializer with activities nested
class ProjectSerializer(serializers.ModelSerializer):
    activities = ActivitySerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'status', 'progress', 'start_date', 'end_date', 'activities']

# Event Serializer
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'event_date', 'location', 'slots']

# Event Registration Serializer
class EventRegistrationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # display username

    class Meta:
        model = EventRegistration
        fields = ['id', 'user', 'event', 'registered_at']

# Notification Serializer
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'title', 'message', 'is_read', 'created_at']
