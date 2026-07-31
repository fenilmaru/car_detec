from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from vehicles.models import Vehicle, VehicleType, Trip
from django.db.models import Count, Q

@login_required
def vehicle_list(request):
    vehicles = Vehicle.objects.select_related('vehicle_type', 'owner').all()
    search = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')
    if search:
        vehicles = vehicles.filter(Q(license_plate__icontains=search) | Q(make__icontains=search) | Q(model__icontains=search))
    if status_filter:
        vehicles = vehicles.filter(status=status_filter)
    types = VehicleType.objects.filter(is_active=True)
    return render(request, 'vehicles/list.html', {'vehicles': vehicles, 'types': types, 'search': search, 'status_filter': status_filter})

@login_required
def vehicle_detail(request, pk):
    vehicle = Vehicle.objects.select_related('vehicle_type', 'owner').get(pk=pk)
    recent_trips = vehicle.trips.order_by('-start_time')[:10]
    cameras = vehicle.cameras.all()
    recent_detections = vehicle.detection_logs.order_by('-created_at')[:10]
    accidents = vehicle.accidents.order_by('-reported_at')[:5]
    context = {'vehicle': vehicle, 'recent_trips': recent_trips, 'cameras': cameras, 'recent_detections': recent_detections, 'accidents': accidents}
    return render(request, 'vehicles/detail.html', context)
