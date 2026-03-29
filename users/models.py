from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model that extends Django's built-in AbstractUser.

    Why extend AbstractUser instead of using it directly?
    Because we need to add a 'role' field for Role-Based Access Control (RBAC).
    RBAC means different users get different permissions based on their role.

    Three roles:
    - citizen  → submits and tracks service requests
    - officer  → reviews and processes service requests
    - admin    → full system access
    """

    ROLE_CHOICES = [
        ('citizen', 'Citizen'),
        ('officer', 'Officer'),
        ('admin', 'Admin'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='citizen',
        help_text="Determines what the user can see and do in the system."
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Optional contact phone number."
    )

    national_id = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        unique=True,  # No two users can share the same national ID
        help_text="National ID number for identity verification."
    )

    def __str__(self):
        return f"{self.username} ({self.role})"

    # Helper methods — used in views to check roles cleanly
    def is_citizen(self):
        return self.role == 'citizen'

    def is_officer(self):
        return self.role == 'officer'

    def is_admin_user(self):
        return self.role == 'admin'
