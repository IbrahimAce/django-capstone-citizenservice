from django.urls import path
from .views import RegisterView, ProfileView

urlpatterns = [
    # POST /api/auth/register/  → create a new account
    path('register/', RegisterView.as_view(), name='register'),

    # GET  /api/auth/profile/   → view your profile
    # PATCH /api/auth/profile/  → update your profile
    path('profile/', ProfileView.as_view(), name='profile'),
]
