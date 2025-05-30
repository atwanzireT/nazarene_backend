from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('full_name', 'phone_number', 'role', 'is_approved')}),
    )
    list_display = ('username', 'full_name', 'email', 'role', 'is_approved')

admin.site.register(Project)
admin.site.register(Activity)
admin.site.register(Event)
admin.site.register(EventRegistration)
admin.site.register(Notification)
admin.site.register(AccountApplication)
admin.site.register(UserActivity)
admin.site.register(ExecutiveTeamMember)
