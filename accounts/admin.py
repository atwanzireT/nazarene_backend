from django.contrib import admin
from .models import AccountApplication, ClassLevel

# Register your models here.
admin.site.register(ClassLevel)
admin.site.register(AccountApplication)