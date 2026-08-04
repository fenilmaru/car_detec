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
    path('auth/', include("autonomous_activation_system.authentication.urls")),
    path('vehicles/', include("autonomous_activation_system.vehicles.urls")),
    path('drivers/', include("autonomous_activation_system.drivers.urls")),
    path('camera/', include("autonomous_activation_system.camera.urls")),
    path('tracking/', include("autonomous_activation_system.tracking.urls")),
    path('accidents/', include("autonomous_activation_system.accidents.urls")),
    path('emergency/', include("autonomous_activation_system.emergency.urls")),
    path('reports/', include("autonomous_activation_system.reports.urls")),
    path('analytics/', include("autonomous_activation_system.analytics.urls")),
    path('notifications/', include("autonomous_activation_system.notifications.urls")),

    # API URLs
    path('api/', include("autonomous_activation_system.api.urls")),
    path(
        'api/auth/',
        include('autonomous_activation_system.authentication.api_urls'),
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
