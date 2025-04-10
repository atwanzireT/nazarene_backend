from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Project, Activity, Event, EventRegistration, Notification, AccountApplication

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('full_name', 'phone_number', 'is_approved')}),
    )
    list_display = ('username', 'full_name', 'email', 'is_approved')

admin.site.register(Project)
admin.site.register(Activity)
admin.site.register(Event)
admin.site.register(EventRegistration)
admin.site.register(Notification)
admin.site.register(AccountApplication)
