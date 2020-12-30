import pandas as pd
from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()
from .models import UserProfile

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'last_login', 'date_joined')
    fieldsets = (
        ('Personal info', {'fields': ('username', 'password', 'role')}),
        ('Important dates', {'fields': ('last_login', 'date_joined', )}),
    )

# admin.site.unregister(User)
# admin.site.register(User, CustomUserAdmin)

admin.site.register(UserProfile)