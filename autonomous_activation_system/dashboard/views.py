from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from vehicles.models import Vehicle
from drivers.models import Driver
from accidents.models import Accident
from camera.models import DetectionLog
from notifications.models import Notification
from tracking.models import GPSLocation
from emergency.models import SOSAlert
from django.db.models import Count, Q, Avg
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder
from datetime import timedelta
import json

def home_view(request):
    if request.user.is_authenticated:
        return render(request, 'dashboard/index.html')
    return render(request, 'partials/login.html')

@login_required
def dashboard_view(request):
    now = timezone.now()
    seven_days_ago = now - timedelta(days=7)
    thirty_days_ago = now - timedelta(days=30)

    # Stats
    total_vehicles = Vehicle.objects.count()
    active_vehicles = Vehicle.objects.filter(status='active').count()
    total_drivers = Driver.objects.count()
    active_drivers = Driver.objects.filter(status='active').count()
    total_accidents = Accident.objects.count()
    recent_accidents = Accident.objects.filter(reported_at__gte=seven_days_ago).count()
    active_alerts = SOSAlert.objects.filter(status='active').count()
    pending_notifications = Notification.objects.filter(is_read=False).count()

    # Recent detections
    recent_detections = DetectionLog.objects.select_related('vehicle', 'camera').order_by('-created_at')[:10]

    # Recent accidents
    recent_accidents_list = Accident.objects.select_related('vehicle').order_by('-reported_at')[:5]

    # Vehicle status breakdown
    vehicle_status = list(Vehicle.objects.values('status').annotate(count=Count('id')))

    # Detection type breakdown
    detection_breakdown = list(DetectionLog.objects.values('detection_type').annotate(count=Count('id'))[:10])

    # GPS locations for active vehicles
    active_vehicle_ids = Vehicle.objects.filter(status='active').values_list('id', flat=True)[:20]
    latest_gps = []
    for vid in active_vehicle_ids:
        loc = GPSLocation.objects.filter(vehicle_id=vid).first()
        if loc:
            latest_gps.append({
                'vehicle': loc.vehicle.license_plate,
                'latitude': float(loc.latitude),
                'longitude': float(loc.longitude),
                'speed': float(loc.speed),
            })

    # Weekly activity
    weekly_activity = []
    for i in range(7):
        day = now - timedelta(days=6-i)
        day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        count = DetectionLog.objects.filter(created_at__gte=day_start, created_at__lt=day_end).count()
        weekly_activity.append({
            'day': day.strftime('%A')[:3],
            'count': count,
        })

    context = {
        'stats': {
            'total_vehicles': total_vehicles,
            'active_vehicles': active_vehicles,
            'total_drivers': total_drivers,
            'active_drivers': active_drivers,
            'total_accidents': total_accidents,
            'recent_accidents': recent_accidents,
            'active_alerts': active_alerts,
            'pending_notifications': pending_notifications,
        },
        'recent_detections': recent_detections,
        'recent_accidents': recent_accidents_list,
        'vehicle_status': vehicle_status,
        'detection_breakdown': json.dumps(detection_breakdown, cls=DjangoJSONEncoder),
        'latest_gps': json.dumps(latest_gps, cls=DjangoJSONEncoder),
        'weekly_activity': json.dumps(weekly_activity, cls=DjangoJSONEncoder),
    }

    return render(request, 'dashboard/index.html', context)
