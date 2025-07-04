from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.core.mail import send_mail
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.shortcuts import render
from .models import *
from .serializers import *
from datetime import datetime, timedelta
from django.utils.timezone import now


# --------------------------------------------
# User (Admin only)
# --------------------------------------------
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_approved', 'role']
    search_fields = ['full_name', 'email', 'username']
    ordering_fields = ['date_joined', 'full_name']
    ordering = ['-date_joined']


# --------------------------------------------
# Projects (Public Read)
# --------------------------------------------
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['status', 'is_featured']
    search_fields = ['title', 'description']

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.query_params.get('active') == 'true':
            from django.utils import timezone
            today = timezone.now().date()
            queryset = queryset.filter(start_date__lte=today, end_date__gte=today)
        return queryset


class ProjectImageViewSet(viewsets.ModelViewSet):
    queryset = ProjectImage.objects.all()
    serializer_class = ProjectImageSerializer
    permission_classes = [permissions.IsAuthenticated]

# --------------------------------------------
# Activities (Public Read)
# --------------------------------------------
class ActivityViewSet(viewsets.ModelViewSet):
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['project']

    def get_queryset(self):
        return Activity.objects.all().order_by('-activity_date')


class ActivityImageViewSet(viewsets.ModelViewSet):
    queryset = ActivityImage.objects.all()
    serializer_class = ActivityImageSerializer
    permission_classes = [permissions.IsAdminUser]


# --------------------------------------------
# Events (Public Read)
# --------------------------------------------
class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['event_date', 'title']
    ordering = ['-event_date']

    def get_queryset(self):
        queryset = Event.objects.all()
        from django.utils import timezone
        if self.request.query_params.get('upcoming') == 'true':
            queryset = queryset.filter(event_date__gte=timezone.now())
        elif self.request.query_params.get('past') == 'true':
            queryset = queryset.filter(event_date__lt=timezone.now())
        return queryset


class EventImageViewSet(viewsets.ModelViewSet):
    queryset = EventImage.objects.all()
    serializer_class = EventImageSerializer
    permission_classes = [permissions.IsAdminUser]


# --------------------------------------------
# Event Registrations (Authenticated only)
# --------------------------------------------
class EventRegistrationViewSet(viewsets.ModelViewSet):
    serializer_class = EventRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return EventRegistration.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# --------------------------------------------
# Notifications (Authenticated only)
# --------------------------------------------
class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['is_read']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        count = Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return Response({'message': f'{count} notifications marked as read'})


# --------------------------------------------
# Docs
# --------------------------------------------
def index(request):
    return render(request, 'api_docs.html')


class ExecutiveTeamMemberViewSet(viewsets.ModelViewSet):
    serializer_class = ExecutiveTeamMemberSerializer

    def get_queryset(self):
        queryset = ExecutiveTeamMember.objects.all().order_by('rank')
        active_param = self.request.query_params.get('active')

        if active_param is not None:
            if active_param.lower() == 'true':
                queryset = queryset.filter(active=True)
            elif active_param.lower() == 'false':
                queryset = queryset.filter(active=False)

        return queryset
        

class ContactMessageViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all().order_by('-submitted_at')
    serializer_class = ContactMessageSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            app = serializer.save()

            # Email to Admin
            send_mail(
                subject='New Contact Message Submitted',
                message=(
                    f'New message from {app.name}\n'
                    f'Email: {app.email}\n'
                    f'Category: {app.get_category_display()}\n'
                    f'Subject: {app.subject or "N/A"}\n\n'
                    f'Message:\n{app.message}'
                ),
                from_email=app.email,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=False,
            )

            # Acknowledgment to User
            send_mail(
                subject='We’ve Received Your Message',
                message=(
                    f'Dear {app.name},\n\n'
                    f'Thank you for contacting us. We’ve received your message and will respond as soon as possible.\n\n'
                    f'Best regards,\nAlumni Relations Team'
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[app.email],
                fail_silently=False,
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

