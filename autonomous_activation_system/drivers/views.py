from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from drivers.models import Driver, DriverHealth
from django.db.models import Q

@login_required
def driver_dashboard(request):
    drivers = Driver.objects.select_related('user').all()
    search = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')
    if search:
        drivers = drivers.filter(Q(user__username__icontains=search) | Q(license_number__icontains=search))
    if status_filter:
        drivers = drivers.filter(status=status_filter)
    context = {'drivers': drivers, 'search': search, 'status_filter': status_filter}
    return render(request, 'drivers/dashboard.html', context)

@login_required
def driver_detail(request, pk):
    driver = Driver.objects.select_related('user').get(pk=pk)
    health_records = driver.health_records.order_by('-recorded_at')[:10]
    trips = driver.trips.order_by('-start_time')[:10]
    context = {'driver': driver, 'health_records': health_records, 'trips': trips}
    return render(request, 'drivers/detail.html', context)
