import django_filters
from .models import ServiceRequest


class ServiceRequestFilter(django_filters.FilterSet):
    """
    Enables URL-based filtering on the service requests list endpoint.

    How it works:
    The citizen or officer adds query parameters to the URL:
      GET /api/requests/?status=pending
      GET /api/requests/?priority=high
      GET /api/requests/?status=in_review&priority=medium
      GET /api/requests/?category=2

    django_filters reads these parameters and builds the SQL WHERE clause automatically.
    """

    status = django_filters.ChoiceFilter(choices=ServiceRequest.STATUS_CHOICES)
    priority = django_filters.ChoiceFilter(choices=ServiceRequest.PRIORITY_CHOICES)

    # Filter by category ID (e.g. ?category=3)
    category = django_filters.NumberFilter(field_name='category__id')

    class Meta:
        model = ServiceRequest
        fields = ['status', 'priority', 'category']
