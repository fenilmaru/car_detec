from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg, Sum, Q
<<<<<<< HEAD
from django.core.serializers.json import DjangoJSONEncoder
=======
<<<<<<< HEAD
from django.core.serializers.json import DjangoJSONEncoder
from vehicles.models import Vehicle, Trip
from accidents.models import Accident
from camera.models import DetectionLog
from notifications.models import Notification
=======
>>>>>>> 1351bb7ec33ebcee08f85bf8ef466dcda7cf2073
from autonomous_activation_system.vehicles.models import Vehicle, Trip
from autonomous_activation_system.accidents.models import Accident
from autonomous_activation_system.camera.models import DetectionLog
from autonomous_activation_system.notifications.models import Notification
<<<<<<< HEAD
=======
>>>>>>> bc576b54091f55fc632f55837fcdde4d6611e04c
>>>>>>> 1351bb7ec33ebcee08f85bf8ef466dcda7cf2073
from django.utils import timezone
from datetime import timedelta
import json

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
        'severity_breakdown': json.dumps(severity_breakdown, cls=DjangoJSONEncoder),
        'detection_breakdown': json.dumps(detection_breakdown, cls=DjangoJSONEncoder),
        'vehicle_activity': vehicle_activity,
    }
    return render(request, 'reports/index.html', context)
