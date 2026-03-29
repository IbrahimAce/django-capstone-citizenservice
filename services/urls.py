from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServiceRequestViewSet, ServiceCategoryViewSet

"""
DRF's DefaultRouter automatically creates all the standard URL patterns
for each ViewSet registered here.

For ServiceRequestViewSet it creates:
  /api/requests/           GET (list), POST (create)
  /api/requests/{id}/      GET (retrieve), PUT/PATCH (update), DELETE
  /api/requests/my/        GET (custom action)

For ServiceCategoryViewSet it creates:
  /api/categories/         GET (list)
  /api/categories/{id}/    GET (retrieve)
"""

router = DefaultRouter()
router.register(r'requests', ServiceRequestViewSet, basename='servicerequest')
router.register(r'categories', ServiceCategoryViewSet, basename='servicecategory')

urlpatterns = [
    path('', include(router.urls)),
]
