from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .api_views import (
    UserViewSet, AccountApplicationViewSet,
    ProjectViewSet, ActivityViewSet,
    EventViewSet, EventRegistrationViewSet,
    NotificationViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'applications', AccountApplicationViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'activities', ActivityViewSet)
router.register(r'events', EventViewSet)
router.register(r'registrations', EventRegistrationViewSet)
router.register(r'notifications', NotificationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
