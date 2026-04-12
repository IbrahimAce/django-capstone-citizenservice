from django.urls import path
from .officer_views import officer_dashboard, request_detail

urlpatterns = [
    path('dashboard/', officer_dashboard, name='officer_dashboard'),
    path('requests/<int:pk>/', request_detail, name='officer_request_detail'),
]
