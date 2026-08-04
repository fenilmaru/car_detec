from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from autonomous_activation_system.tracking.models import GPSLocation, RouteHistory
from autonomous_activation_system.vehicles.models import Vehicle
import json


@login_required
def tracking_view(request):
    active_vehicles = Vehicle.objects.filter(status='active')
    gps_locations = []
    gps_markers = []
    for v in active_vehicles[:30]:
        loc = GPSLocation.objects.filter(vehicle=v).first()
        if loc:
            gps_locations.append(loc)
            gps_markers.append({
                'vehicle': v.license_plate,
                'latitude': float(loc.latitude),
                'longitude': float(loc.longitude),
                'speed': float(loc.speed),
                'heading': float(loc.heading) if loc.heading is not None else None,
                'timestamp': loc.timestamp.isoformat(),
            })
    context = {
        'gps_locations': gps_locations,
        'gps_markers_json': json.dumps(gps_markers, cls=DjangoJSONEncoder),
        'active_vehicles': active_vehicles,
    }
    return render(request, 'tracking/index.html', context)

@login_required
def route_history_view(request):
    routes = RouteHistory.objects.select_related('vehicle').order_by('-start_time')[:50]
    return render(request, 'tracking/routes.html', {'routes': routes})
