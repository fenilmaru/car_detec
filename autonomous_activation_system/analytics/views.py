from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg, Sum, Q
<<<<<<< HEAD
from django.core.serializers.json import DjangoJSONEncoder
=======
<<<<<<< HEAD
from django.core.serializers.json import DjangoJSONEncoder
from vehicles.models import Vehicle, Trip
from drivers.models import Driver
from accidents.models import Accident
from camera.models import DetectionLog
from tracking.models import GPSLocation
=======
>>>>>>> 1351bb7ec33ebcee08f85bf8ef466dcda7cf2073
from autonomous_activation_system.vehicles.models import Vehicle, Trip
from autonomous_activation_system.drivers.models import Driver
from autonomous_activation_system.accidents.models import Accident
from autonomous_activation_system.camera.models import DetectionLog
from autonomous_activation_system.tracking.models import GPSLocation
<<<<<<< HEAD
=======
>>>>>>> bc576b54091f55fc632f55837fcdde4d6611e04c
>>>>>>> 1351bb7ec33ebcee08f85bf8ef466dcda7cf2073
from django.utils import timezone
from datetime import timedelta, datetime
import json

@login_required
def analytics_view(request):
    now = timezone.now()
    thirty = now - timedelta(days=30)

    # Fleet utilization
    total_vehicles = Vehicle.objects.count()
    active_vehicles = Vehicle.objects.filter(status='active').count()
    utilization = (active_vehicles / total_vehicles * 100) if total_vehicles > 0 else 0

    # Driver performance
    top_drivers = Driver.objects.annotate(trip_count=Count('trips')).order_by('-trip_count')[:10]

    # Safety metrics
    accidents_by_severity = list(Accident.objects.filter(reported_at__gte=thirty).values('severity').annotate(count=Count('id')))
    detections_by_type = list(DetectionLog.objects.filter(created_at__gte=thirty).values('detection_type').annotate(count=Count('id')))
    critical_events = DetectionLog.objects.filter(severity='critical', created_at__gte=thirty).count()

    # Daily trends
    daily_detections = []
    for i in range(30):
        day = now - timedelta(days=29-i)
        day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        count = DetectionLog.objects.filter(created_at__gte=day_start, created_at__lt=day_end).count()
        daily_detections.append({'date': day.strftime('%m/%d'), 'count': count})

    # Trip stats
    total_trips = Trip.objects.filter(start_time__gte=thirty).count()
    completed_trips = Trip.objects.filter(start_time__gte=thirty, status='completed').count()

    context = {
        'utilization': round(utilization, 1),
        'top_drivers': top_drivers,
        'accidents_by_severity': json.dumps(accidents_by_severity, cls=DjangoJSONEncoder),
        'detections_by_type': json.dumps(detections_by_type, cls=DjangoJSONEncoder),
        'critical_events': critical_events,
        'daily_detections': json.dumps(daily_detections, cls=DjangoJSONEncoder),
        'total_trips': total_trips,
        'completed_trips': completed_trips,
    }
    return render(request, 'analytics/index.html', context)
