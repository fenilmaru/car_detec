from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    # Vehicles
    path('vehicles/', views.VehicleListCreateAPI.as_view(), name='vehicle-list'),
    path('vehicles/<uuid:pk>/', views.VehicleDetailAPI.as_view(), name='vehicle-detail'),
    path('vehicle-types/', views.VehicleTypeListAPI.as_view(), name='vehicle-types'),

    # Drivers
    path('drivers/', views.DriverListCreateAPI.as_view(), name='driver-list'),
    path('drivers/<uuid:pk>/', views.DriverDetailAPI.as_view(), name='driver-detail'),

    # Trips
    path('trips/', views.TripListCreateAPI.as_view(), name='trip-list'),
    path('trips/<uuid:pk>/', views.TripDetailAPI.as_view(), name='trip-detail'),

    # Accidents
    path('accidents/', views.AccidentListCreateAPI.as_view(), name='accident-list'),
    path('accidents/<uuid:pk>/', views.AccidentDetailAPI.as_view(), name='accident-detail'),

    # Cameras
    path('cameras/', views.CameraListCreateAPI.as_view(), name='camera-list'),
    path('cameras/<uuid:pk>/', views.CameraDetailAPI.as_view(), name='camera-detail'),

    # Detections
    path('detections/', views.DetectionLogListAPI.as_view(), name='detection-list'),

    # GPS
    path('gps/', views.GPSLocationListAPI.as_view(), name='gps-list'),

    # Emergency
    path('sos/', views.SOSAlertListCreateAPI.as_view(), name='sos-list'),
    path('sos/<uuid:pk>/', views.SOSAlertDetailAPI.as_view(), name='sos-detail'),
    path('emergency-services/', views.EmergencyServiceListAPI.as_view(), name='emergency-services'),

    # Notifications
    path('notifications/', views.NotificationListAPI.as_view(), name='notification-list'),
    path('notifications/<uuid:pk>/read/', views.mark_notification_read, name='notification-read'),

    # Analytics
    path('analytics/', views.analytics_overview, name='analytics'),

    # Reports
    path('reports/', views.generate_report, name='reports'),
]
