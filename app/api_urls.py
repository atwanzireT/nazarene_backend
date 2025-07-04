from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()

# ViewSets
router.register('users', api_views.UserViewSet, basename='user')
router.register('projects', api_views.ProjectViewSet, basename='project')
router.register('project-images', api_views.ProjectImageViewSet, basename='project-image')
router.register('activities', api_views.ActivityViewSet, basename='activity')
router.register('activity-images', api_views.ActivityImageViewSet, basename='activity-image')
router.register('events', api_views.EventViewSet, basename='event')
router.register('event-images', api_views.EventImageViewSet, basename='event-image')
router.register('registrations', api_views.EventRegistrationViewSet, basename='eventregistration')
router.register('notifications', api_views.NotificationViewSet, basename='notification')
router.register('executive-team', api_views.ExecutiveTeamMemberViewSet, basename="executive-team")
router.register('contact-messages', api_views.ContactMessageViewSet, basename='contactmessage')

urlpatterns = [
    path('', include(router.urls)),
]
