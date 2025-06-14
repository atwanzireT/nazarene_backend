from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from app.models import Event, Notification, User

class Command(BaseCommand):
    help = 'Creates notifications for events starting within 1 month'

    def handle(self, *args, **options):
        now = timezone.now()
        one_month_later = now + timedelta(days=30)
        
        # Get upcoming events within 1 month
        upcoming_events = Event.objects.filter(
            event_date__gt=now,
            event_date__lte=one_month_later,
            status='upcoming'
        )
        
        for event in upcoming_events:
            # Calculate time left
            time_left = event.event_date - now
            days = time_left.days
            hours = time_left.seconds // 3600
            
            # Create notifications for all users
            for user in User.objects.filter(is_active=True):
                Notification.objects.update_or_create(
                    user=user,
                    event=event,
                    defaults={
                        'title': f"Upcoming Event: {event.title}",
                        'message': f"Starts in {days} days and {hours} hours",
                        'type': 'event',
                        'time_left': f"{days} days, {hours} hours"
                    }
                )
        
        self.stdout.write(self.style.SUCCESS('Successfully created event notifications'))