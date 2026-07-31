from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from emergency.models import SOSAlert, EmergencyContact, EmergencyService

@login_required
def emergency_view(request):
    active_alerts = SOSAlert.objects.filter(status='active').order_by('-created_at')
    resolved_alerts = SOSAlert.objects.filter(status='resolved').order_by('-created_at')[:10]
    emergency_services = EmergencyService.objects.filter(is_active=True)
    return render(request, 'emergency/index.html', {
        'active_alerts': active_alerts, 'resolved_alerts': resolved_alerts,
        'emergency_services': emergency_services
    })

@login_required
def sos_contacts(request):
    contacts = EmergencyContact.objects.filter(user=request.user)
    services = EmergencyService.objects.filter(is_active=True)
    return render(request, 'emergency/contacts.html', {'contacts': contacts, 'services': services})
