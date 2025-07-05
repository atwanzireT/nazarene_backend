from django.urls import path
from . import views
from .views import user_login
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),

    # User management
    path('users/', views.user_list, name='user_list'),
    path('login-activities/', views.user_login_activities, name='login_activities'),

    # Account Applications
    path('account-applications/', views.account_application_list, name='account_application_list'),
    path('account-application/<int:application_id>/', views.account_application_detail, name='account_application_detail'),
    path('applications/<int:application_id>/approve/', views.approve_account_application, name='approve_application'),
 
    # Projects and Activities
    path('projects/', views.project_list, name='project_list'),
    path('create-project/', views.create_project, name='create_project'),
    path('activities/', views.activity_list, name='activity_list'),
    path('create-activity/', views.create_activity, name='create_activity'),

    # Events and Registrations
    path('events/', views.event_list, name='event_list'),
    path('create-event/', views.create_event, name='create_event'),
    path('event-registrations/', views.event_registration_list, name='event_registration_list'),
    path('register-event/<int:event_id>/', views.register_event, name='register_event'),

    # Notifications
    path('notifications/', views.notification_list, name='notification_list'),
    path('create-notification/', views.create_notification, name='create_notification'),
    
    # Auth
    path('accounts/login/', user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Staff
    path('executive-team/', views.executive_team_list, name='executive_team_list'),
    path('executive-team/create/', views.executive_team_create, name='executive_team_create'),
    
    # Images
    path('projects/<int:project_id>/add-image/', views.add_project_image, name='add_project_image'),
    path('events/<int:event_id>/add-image/', views.add_event_image, name='add_event_image'),
    path('activities/<int:activity_id>/add-image/', views.add_activity_image, name='add_activity_image'),
]
