from django.shortcuts import render
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import (
    AccountApplication, Project, Activity,
    Event, EventRegistration, Notification, User
)
from .serializers import (
    AccountApplicationSerializer, ProjectSerializer,
    ActivitySerializer, EventSerializer,
    EventRegistrationSerializer, NotificationSerializer,
    UserSerializer
)

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_approved', 'role']
    search_fields = ['full_name', 'email', 'username']
    ordering_fields = ['date_joined', 'full_name']
    ordering = ['-date_joined']


class AccountApplicationListView(generics.ListAPIView):
    queryset = AccountApplication.objects.all()
    serializer_class = AccountApplicationSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['is_approved', 'year_joined_jonahs', 'year_left_jonahs']
    search_fields = ['full_first_name', 'full_surname', 'email']


class ProjectListView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['status']
    search_fields = ['title', 'description']

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.query_params.get('status', None)
        
        # Filter for active projects
        if self.request.query_params.get('active') == 'true':
            from django.utils import timezone
            today = timezone.now().date()
            queryset = queryset.filter(
                start_date__lte=today,
                end_date__gte=today
            )
        
        return queryset


class ActivityListView(generics.ListAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['project']

    def get_queryset(self):
        queryset = Activity.objects.all()
        project_id = self.request.query_params.get('project', None)
        
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        
        return queryset.order_by('-activity_date')


class EventListView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['event_date', 'title']
    ordering = ['-event_date']

    def get_queryset(self):
        queryset = Event.objects.all()
        
        # Filter for upcoming events
        if self.request.query_params.get('upcoming') == 'true':
            from django.utils import timezone
            queryset = queryset.filter(event_date__gte=timezone.now())
        
        # Filter for past events
        if self.request.query_params.get('past') == 'true':
            from django.utils import timezone
            queryset = queryset.filter(event_date__lt=timezone.now())
        
        return queryset


class EventRegistrationListView(generics.ListAPIView):
    serializer_class = EventRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users can only see their own registrations
        return EventRegistration.objects.filter(user=self.request.user)


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['is_read']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        # Users can only see their own notifications
        return Notification.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        updated = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).update(is_read=True)
        
        return Response({
            'status': 'success',
            'message': f'{updated} notifications marked as read'
        })


class AccountApplicationAPIView(APIView):
    # permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = AccountApplicationSerializer(data=request.data)
        if serializer.is_valid():
            app = serializer.save()
            
            # Send email to admin
            send_mail(
                'New Account Application Submitted',
                f'New application from {app.full_first_name} {app.full_surname}\n'
                f'Email: {app.email}\n'
                f'Phone: {app.mobile_phone_1}\n'
                f'Year Joined: {app.year_joined_jonahs}',
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL],
                fail_silently=False,
            )
            
            # Optional: Send confirmation email to applicant
            send_mail(
                'Application Received',
                f'Dear {app.full_first_name},\n\n'
                f'Thank you for submitting your application to the Jonahs Alumni Association. '
                f'We have received your details and will review them shortly.\n\n'
                f'You will receive another email once your application has been processed.\n\n'
                f'Best regards,\n'
                f'The Alumni Team',
                settings.DEFAULT_FROM_EMAIL,
                [app.email],
                fail_silently=False,
            )
            
            return Response(
                {'message': 'Application submitted successfully'}, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

# Api Docs
def index(request):
    return render(request, 'api_docs.html')