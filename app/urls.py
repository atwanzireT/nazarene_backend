from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # User management
    path('users/', views.user_list, name='user_list'),
    path('register-user/', views.register_user, name='register_user'),
    path('login-activities/', views.user_login_activities, name='login_activities'),

    # Account Applications
    path('account-application/create/', views.account_application_create, name='account_application_create'),
    path('account-applications/', views.account_application_list, name='account_application_list'),
    path('account-application/<int:application_id>/', views.account_application_detail, name='account_application_detail'),
    path('apply-account/', views.apply_account, name='apply_account'),
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
]
