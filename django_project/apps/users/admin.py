from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_editor', 'is_admin', 'is_active')
    list_filter = ('is_editor', 'is_admin', 'is_active')

    fieldsets = UserAdmin.fieldsets + (
        ('Role Permissions', {'fields': ('is_editor', 'is_admin')}),
    )