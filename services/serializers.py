from rest_framework import serializers
from .models import ServiceRequest, ServiceCategory


class ServiceCategorySerializer(serializers.ModelSerializer):
    """Simple read-only serializer for listing service categories."""

    class Meta:
        model = ServiceCategory
        fields = ['id', 'name', 'description']


class ServiceRequestSerializer(serializers.ModelSerializer):
    """
    Full serializer used when READING service requests (GET).

    Extra read-only fields:
    - citizen_username    → shows the username, not just the integer ID
    - category_name       → shows the category name, not just the integer ID
    - assigned_officer_username → officer name if assigned

    These use serializer.SerializerMethodField / source= shortcut.
    The source='citizen.username' means: follow the ForeignKey to citizen, then get .username
    """

    citizen_username = serializers.CharField(
        source='citizen.username',
        read_only=True
    )
    category_name = serializers.CharField(
        source='category.name',
        read_only=True
    )
    assigned_officer_username = serializers.CharField(
        source='assigned_officer.username',
        read_only=True,
        default=None
    )

    class Meta:
        model = ServiceRequest
        fields = [
            'id',
            'title',
            'description',
            'status',
            'priority',
            'category',           # Integer ID (for filtering/updates)
            'category_name',      # Human-readable name (for display)
            'citizen_username',
            'assigned_officer_username',
            'notes',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id', 'citizen_username', 'assigned_officer_username',
            'created_at', 'updated_at'
        ]


class ServiceRequestCreateSerializer(serializers.ModelSerializer):
    """
    Simplified serializer used only when a citizen CREATES a new request (POST).

    Why a separate serializer?
    - Citizens should not be able to set status, notes, or assign officers
    - Keeping it separate is cleaner and more secure than one serializer trying to do both
    - This is a deliberate design decision (mentioned in the form submission notes)
    """

    class Meta:
        model = ServiceRequest
        fields = ['title', 'description', 'category', 'priority']
