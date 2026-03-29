from django.db import models
from django.conf import settings


class ServiceCategory(models.Model):
    """
    Represents a type of government service.
    Examples: 'Birth Certificate', 'Land Records', 'Business Permit'

    Managed by admins through the admin panel.
    Citizens choose a category when submitting a request.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Service Categories"
        ordering = ['name']  # Always sorted alphabetically

    def __str__(self):
        return self.name


class ServiceRequest(models.Model):
    """
    A citizen's request for a specific government service.

    Key design decisions:
    - ForeignKey to User (citizen) — one citizen, many requests (one-to-many)
    - ForeignKey to User (officer) — officer assigned to handle it (nullable)
    - ForeignKey to ServiceCategory — what type of service is being requested
    - status field — tracks the request through its lifecycle
    - PROTECT on category — prevents accidentally deleting a category that has requests
    """

    STATUS_CHOICES = [
        ('pending', 'Pending'),       # Just submitted, waiting to be reviewed
        ('in_review', 'In Review'),   # Officer is actively reviewing
        ('approved', 'Approved'),     # Approved but not yet completed
        ('rejected', 'Rejected'),     # Denied with reason in notes
        ('completed', 'Completed'),   # Fully processed and done
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    citizen = models.ForeignKey(
        settings.AUTH_USER_MODEL,   # Refers to our custom User model
        on_delete=models.CASCADE,   # Delete requests if citizen account is deleted
        related_name='service_requests',
        limit_choices_to={'role': 'citizen'},
    )

    assigned_officer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,  # If officer account deleted, keep the request (set to null)
        null=True,
        blank=True,
        related_name='assigned_requests',
        limit_choices_to={'role': 'officer'},
    )

    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.PROTECT,   # Cannot delete a category that has active requests
        related_name='requests',
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium'
    )
    notes = models.TextField(
        blank=True,
        help_text="Officer notes or rejection reason — not editable by citizens."
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Updates automatically on every save

    class Meta:
        ordering = ['-created_at']  # Newest requests appear first

    def __str__(self):
        return f"[{self.status.upper()}] {self.title} — {self.citizen.username}"
