from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg, Sum, Q
from vehicles.models import Vehicle, Trip
from accidents.models import Accident
from camera.models import DetectionLog
from notifications.models import Notification
from django.utils import timezone
from datetime import timedelta

@login_required
def reports_view(request):
    now = timezone.now()
    period = request.GET.get('period', 'week')
    if period == 'day':
        start = now - timedelta(days=1)
    elif period == 'month':
        start = now - timedelta(days=30)
    elif period == 'year':
        start = now - timedelta(days=365)
    else:
        start = now - timedelta(days=7)

    trips = Trip.objects.filter(start_time__gte=start).count()
    accidents = Accident.objects.filter(reported_at__gte=start).count()
    detections = DetectionLog.objects.filter(created_at__gte=start).count()
    avg_detection = DetectionLog.objects.filter(created_at__gte=start).aggregate(avg_confidence=Avg('confidence_score'))

    severity_breakdown = list(Accident.objects.filter(reported_at__gte=start).values('severity').annotate(count=Count('id')))
    detection_breakdown = list(DetectionLog.objects.filter(created_at__gte=start).values('detection_type').annotate(count=Count('id')))
    vehicle_activity = list(Trip.objects.filter(start_time__gte=start).values('vehicle__license_plate').annotate(trips=Count('id')).order_by('-trips')[:10])

    context = {
        'period': period, 'trips': trips, 'accidents': accidents,
        'detections': detections, 'avg_detection': avg_detection.get('avg_confidence'),
        'severity_breakdown': severity_breakdown,
        'detection_breakdown': detection_breakdown,
        'vehicle_activity': vehicle_activity,
    }
    return render(request, 'reports/index.html', context)
