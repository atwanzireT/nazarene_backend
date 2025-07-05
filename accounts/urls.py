from django.urls import path
from . import views


urlpatterns = [
    path("signup/", views.signup_view, name="signup"),
     # Account Applications
    path('account-application/create/', views.account_application_create, name='account_application_create'),
    path('apply-account/', views.apply_account, name='apply_account'),
    path('account-applications/success/', views.account_application_success, name='account-application-success'),

]