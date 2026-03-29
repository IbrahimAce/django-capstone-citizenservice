from django.contrib import admin
from .models import ServiceRequest, ServiceCategory


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    """Admin interface for managing service categories."""
    list_display = ['name', 'created_at']
    search_fields = ['name']


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    """Admin interface for managing all service requests."""
    list_display = ['title', 'citizen', 'category', 'status', 'priority', 'created_at']
    list_filter = ['status', 'priority', 'category']
    search_fields = ['title', 'citizen__username']
    raw_id_fields = ['citizen', 'assigned_officer']  # Better for large user tables
    readonly_fields = ['created_at', 'updated_at']
