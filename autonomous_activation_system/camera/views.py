from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from autonomous_activation_system.camera.models import Camera, DetectionLog
from django.db.models import Count, Q

@login_required
def camera_view(request):
    cameras = Camera.objects.select_related('vehicle').all()
    detections = DetectionLog.objects.select_related('vehicle', 'camera').order_by('-created_at')[:20]
    return render(request, 'camera/index.html', {'cameras': cameras, 'detections': detections})

@login_required
def camera_detail(request, pk):
    camera = Camera.objects.select_related('vehicle').get(pk=pk)
    detections = camera.detection_logs.order_by('-created_at')[:50]
    return render(request, 'camera/detail.html', {'camera': camera, 'detections': detections})
