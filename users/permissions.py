from rest_framework.permissions import BasePermission


class IsCitizen(BasePermission):
    """
    Custom DRF permission: only allows users whose role is 'citizen'.

    How DRF permissions work:
    - has_permission() is called before the view runs.
    - If it returns False, DRF returns 403 Forbidden automatically.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'citizen'


class IsOfficer(BasePermission):
    """Only allows users whose role is 'officer'."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'officer'


class IsAdminRole(BasePermission):
    """Only allows users whose role is 'admin'."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class IsOfficerOrAdmin(BasePermission):
    """Allows both officers and admins. Used for request management endpoints."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in ['officer', 'admin']
        )
