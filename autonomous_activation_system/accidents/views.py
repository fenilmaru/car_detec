from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accidents.models import Accident

@login_required
def accident_list(request):
    accidents = Accident.objects.select_related('vehicle', 'driver').order_by('-reported_at')
    severity = request.GET.get('severity', '')
    status = request.GET.get('status', '')
    if severity:
        accidents = accidents.filter(severity=severity)
    if status:
        accidents = accidents.filter(status=status)
    return render(request, 'accidents/list.html', {'accidents': accidents, 'severity': severity, 'status': status})

@login_required
def accident_detail(request, pk):
    accident = Accident.objects.select_related('vehicle', 'driver').get(pk=pk)
    images = accident.images.all()
    videos = accident.videos.all()
    return render(request, 'accidents/detail.html', {'accident': accident, 'images': images, 'videos': videos})
