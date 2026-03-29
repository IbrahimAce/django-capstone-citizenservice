from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Registers our custom User model with the Django admin panel.
    Extends the default UserAdmin so we keep the built-in password change form etc.
    We add our custom fields (role, phone_number, national_id) as an extra section.
    """
    list_display = ['username', 'email', 'role', 'is_active', 'date_joined']
    list_filter = ['role', 'is_active']
    search_fields = ['username', 'email']

    # Add our fields to the edit form in admin
    fieldsets = UserAdmin.fieldsets + (
        ('CitizenService Fields', {
            'fields': ('role', 'phone_number', 'national_id')
        }),
    )
