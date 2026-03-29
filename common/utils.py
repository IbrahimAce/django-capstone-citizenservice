"""
Shared utility functions for the CitizenService project.

Why a common app?
DRY principle (Don't Repeat Yourself).
Any helper function that might be needed by more than one app goes here,
rather than duplicating it in each app.
"""

from django.db.models import Count


def get_status_summary(queryset):
    """
    Returns a count of service requests grouped by status.
    Useful for building a dashboard summary.

    Example output:
    [
        {'status': 'pending', 'count': 12},
        {'status': 'approved', 'count': 5},
    ]
    """
    return queryset.values('status').annotate(count=Count('id'))


def format_datetime(dt):
    """
    Returns a human-readable version of a datetime object.
    Example: 'March 29, 2026 at 14:35'
    Returns None if no datetime is provided.
    """
    if dt is None:
        return None
    return dt.strftime('%B %d, %Y at %H:%M')
