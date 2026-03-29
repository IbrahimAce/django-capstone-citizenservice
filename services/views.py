from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import ServiceRequest, ServiceCategory
from .serializers import (
    ServiceRequestSerializer,
    ServiceRequestCreateSerializer,
    ServiceCategorySerializer,
)
from .filters import ServiceRequestFilter

# TODO (April 16): Move status-change email alerts to Celery async tasks
# TODO (April 16): Replace locmem cache with Redis for shared caching across workers


class ServiceCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only endpoints for listing service categories.

    GET /api/categories/      → list all categories (paginated)
    GET /api/categories/{id}/ → retrieve a single category

    ReadOnlyModelViewSet = only GET endpoints, no create/update/delete.
    Categories are managed by admins through the admin panel.
    """
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class ServiceRequestViewSet(viewsets.ModelViewSet):
    """
    Full CRUD API for service requests with Role-Based Access Control.

    Auto-generated endpoints by ModelViewSet + DRF Router:
    GET    /api/requests/          → list (filtered by role)
    POST   /api/requests/          → create new request
    GET    /api/requests/{id}/     → retrieve single request
    PUT    /api/requests/{id}/     → full update
    PATCH  /api/requests/{id}/     → partial update
    DELETE /api/requests/{id}/     → delete

    Custom endpoint:
    GET    /api/requests/my/       → citizen's own requests
    """

    filterset_class = ServiceRequestFilter
    permission_classes = [permissions.IsAuthenticated]

    # Enables ?search=keyword on title and description fields
    search_fields = ['title', 'description']

    # Enables ?ordering=created_at or ?ordering=-priority
    ordering_fields = ['created_at', 'priority', 'status']

    def get_queryset(self):
        """
        RBAC-aware queryset:
        - Officers and admins → see ALL requests
        - Citizens → see ONLY their own requests

        select_related() is an ORM optimisation.
        Without it, accessing request.citizen.username triggers a separate SQL query
        for each row — this is called the N+1 problem.
        select_related() joins the tables in a single SQL query upfront.
        """
        user = self.request.user

        if user.role in ['officer', 'admin']:
            return ServiceRequest.objects.select_related(
                'citizen', 'assigned_officer', 'category'
            ).all()

        # Citizens only see their own submissions
        return ServiceRequest.objects.select_related(
            'citizen', 'assigned_officer', 'category'
        ).filter(citizen=user)

    def get_serializer_class(self):
        """
        Use the simplified create serializer for POST requests.
        Use the full serializer for everything else (list, retrieve, update).
        """
        if self.action == 'create':
            return ServiceRequestCreateSerializer
        return ServiceRequestSerializer

    def perform_create(self, serializer):
        """
        Called by DRF when a valid POST request is saved.
        We automatically set citizen = the logged-in user.
        This prevents a citizen from creating a request attributed to someone else.
        """
        serializer.save(citizen=self.request.user)

    def update(self, request, *args, **kwargs):
        """
        RBAC enforcement for updates:
        - Citizens: can only edit their own PENDING requests (not in_review, approved, etc.)
        - Officers/Admins: can update status, notes, and assigned_officer freely
        """
        instance = self.get_object()
        user = request.user

        if user.role == 'citizen':
            # Citizens cannot edit requests that belong to someone else
            if instance.citizen != user:
                return Response(
                    {"detail": "You can only edit your own service requests."},
                    status=status.HTTP_403_FORBIDDEN
                )
            # Citizens cannot edit requests that are already being processed
            if instance.status != 'pending':
                return Response(
                    {"detail": "You can only edit requests that are still pending."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Always treat updates as partial (PATCH-style) to avoid requiring all fields
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    @action(detail=False, methods=['get'], url_path='my')
    def my_requests(self, request):
        """
        Custom action: GET /api/requests/my/

        What is @action?
        It adds an extra non-standard endpoint to a ViewSet.
        detail=False means the URL is /requests/my/ not /requests/{id}/my/

        Returns only the logged-in user's own requests, regardless of role.
        Useful for a citizen dashboard that shows "my submissions".
        """
        queryset = ServiceRequest.objects.select_related(
            'citizen', 'assigned_officer', 'category'
        ).filter(citizen=request.user)

        # Apply pagination (uses PAGE_SIZE=10 from settings)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ServiceRequestSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ServiceRequestSerializer(queryset, many=True)
        return Response(serializer.data)
