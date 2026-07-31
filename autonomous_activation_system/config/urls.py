"""
URL Configuration for Autonomous Activation System.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from autonomous_activation_system.dashboard.views import (home_view,dashboard_view,)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('dashboard/', dashboard_view, name='dashboard'),

    # App URLs
    path('auth/', include('authentication.urls')),
    path('vehicles/', include('vehicles.urls')),
    path('drivers/', include('drivers.urls')),
    path('camera/', include('camera.urls')),
    path('tracking/', include('tracking.urls')),
    path('accidents/', include('accidents.urls')),
    path('emergency/', include('emergency.urls')),
    path('reports/', include('reports.urls')),
    path('analytics/', include('analytics.urls')),
    path('notifications/', include('notifications.urls')),

    # API URLs
    path('api/', include('api.urls')),
    path('api/auth/', include('authentication.api_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
