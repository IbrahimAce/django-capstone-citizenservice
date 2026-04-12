from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Homepage
    path('', TemplateView.as_view(template_name='home.html'), name='home'),

    # Auth (API)
    path('api/auth/', include('users.urls')),
    path('api/', include('services.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Web portals (we add these in the next phases)
    path('', include('users.web_urls')),       # login, register, logout
    path('citizen/', include('services.citizen_urls')),  # citizen portal
    path('officer/', include('services.officer_urls')),  # officer portal
]
