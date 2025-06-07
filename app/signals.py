from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import UserActivity

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    UserActivity.objects.create(user=user, activity='login')

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    if user.is_authenticated:
        UserActivity.objects.create(user=user, activity='logout')
