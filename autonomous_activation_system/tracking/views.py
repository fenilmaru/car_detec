from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from autonomous_activation_system.tracking.models import GPSLocation, RouteHistory
from autonomous_activation_system.vehicles.models import Vehicle

@login_required
def tracking_view(request):
    active_vehicles = Vehicle.objects.filter(status='active')
    gps_locations = []
    for v in active_vehicles[:30]:
        loc = GPSLocation.objects.filter(vehicle=v).first()
        if loc:
            gps_locations.append(loc)
    return render(request, 'tracking/index.html', {'gps_locations': gps_locations, 'active_vehicles': active_vehicles})

@login_required
def route_history_view(request):
    routes = RouteHistory.objects.select_related('vehicle').order_by('-start_time')[:50]
    return render(request, 'tracking/routes.html', {'routes': routes})
