from django.urls import path
from .citizen_views import citizen_dashboard, submit_request, request_detail

urlpatterns = [
    path('dashboard/', citizen_dashboard, name='citizen_dashboard'),
    path('submit/', submit_request, name='submit_request'),
    path('requests/<int:pk>/', request_detail, name='citizen_request_detail'),
]
