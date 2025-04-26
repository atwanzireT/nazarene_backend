from django.urls import path, include
from . import api_views
from rest_framework.routers import DefaultRouter
from .api_views import (
    UserListView,
    AccountApplicationListView,
    ProjectListView,
    ActivityListView,
    EventListView,
    EventRegistrationListView,
    NotificationListView,
    AccountApplicationAPIView
)

urlpatterns = [
    # Docs
    path('', api_views.index, name='api-docs'),
    # List views
    path('users/', UserListView.as_view(), name='user-list'),
    path('applications/', AccountApplicationListView.as_view(), name='application-list'),
    path('projects/', ProjectListView.as_view(), name='project-list'),
    path('activities/', ActivityListView.as_view(), name='activity-list'),
    path('events/', EventListView.as_view(), name='event-list'),
    path('registrations/', EventRegistrationListView.as_view(), name='eventregistration-list'),
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    
    # Special endpoints
    path('account-application/', AccountApplicationAPIView.as_view(), name='account-application-api'),
]