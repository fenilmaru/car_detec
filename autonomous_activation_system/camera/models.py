import uuid
from django.db import models
from django.conf import settings

class Camera(models.Model):
    STATUS_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('maintenance', 'Maintenance'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey('vehicles.Vehicle', on_delete=models.CASCADE, related_name='cameras')
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, choices=[
        ('front', 'Front'), ('rear', 'Rear'), ('left', 'Left'),
        ('right', 'Right'), ('interior', 'Interior'), ('dash', 'Dashboard')
    ])
    stream_url = models.URLField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='offline')
    is_active = models.BooleanField(default=True)
    last_frame_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cameras'

    def __str__(self):
        return f"Camera: {self.name} - {self.vehicle.license_plate}"

class DetectionLog(models.Model):
    DETECTION_TYPE = [
        ('object', 'Object Detection'),
        ('lane', 'Lane Detection'),
        ('traffic_sign', 'Traffic Sign Detection'),
        ('seatbelt', 'Seat Belt Detection'),
        ('drowsiness', 'Drowsiness Detection'),
        ('accident', 'Accident Detection'),
        ('helmet', 'Helmet Detection'),
        ('speed', 'Speed Estimation'),
    ]
    SEVERITY = [
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('critical', 'Critical'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey('vehicles.Vehicle', on_delete=models.CASCADE, related_name='detection_logs')
    camera = models.ForeignKey(Camera, on_delete=models.SET_NULL, null=True)
    detection_type = models.CharField(max_length=20, choices=DETECTION_TYPE)
    severity = models.CharField(max_length=20, choices=SEVERITY, default='info')
    description = models.TextField()
    confidence_score = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    bounding_boxes = models.JSONField(default=list, blank=True)
    frame_image = models.ImageField(upload_to='detection_frames/', blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    is_reviewed = models.BooleanField(default=False)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'detection_logs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['detection_type', 'created_at']),
            models.Index(fields=['severity']),
            models.Index(fields=['vehicle', 'created_at']),
        ]

    def __str__(self):
        return f"{self.detection_type}: {self.severity} - {self.vehicle.license_plate}"
