from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/dashboard/$', consumers.DashboardConsumer.as_asgi()),
    re_path(r'ws/gps/(?P<vehicle_id>[^/]+)/$', consumers.GPSConsumer.as_asgi()),
    re_path(r'ws/detections/$', consumers.DetectionConsumer.as_asgi()),
    re_path(r'ws/emergency/$', consumers.EmergencyConsumer.as_asgi()),
]
