from rest_framework import generics, permissions
from .models import User
from .serializers import RegisterSerializer, UserProfileSerializer


class RegisterView(generics.CreateAPIView):
    """
    POST /api/auth/register/

    Public endpoint — no JWT token required to register.
    DRF's CreateAPIView handles the POST request automatically.
    It calls RegisterSerializer.is_valid() and then .save() for us.

    permission_classes = [AllowAny] overrides the global IsAuthenticated default.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    GET   /api/auth/profile/   → returns the logged-in user's data
    PATCH /api/auth/profile/   → updates allowed fields (email, phone, national_id)

    RetrieveUpdateAPIView combines both operations in one class.
    JWT token is required (global default applies here).
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        Override the default behaviour.
        Instead of looking up a user by URL pk (e.g. /profile/5/),
        we always return the currently authenticated user.
        This way users cannot access each other's profiles.
        """
        return self.request.user
