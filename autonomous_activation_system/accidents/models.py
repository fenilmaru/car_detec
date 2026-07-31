import uuid
from django.db import models

class Accident(models.Model):
    SEVERITY_CHOICES = [
        ('minor', 'Minor'),
        ('moderate', 'Moderate'),
        ('severe', 'Severe'),
        ('critical', 'Critical'),
        ('fatal', 'Fatal'),
    ]
    STATUS_CHOICES = [
        ('reported', 'Reported'),
        ('investigating', 'Investigating'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey('vehicles.Vehicle', on_delete=models.CASCADE, related_name='accidents')
    driver = models.ForeignKey('drivers.Driver', on_delete=models.SET_NULL, null=True, related_name='accidents')
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='reported')
    location = models.CharField(max_length=500)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    speed_at_impact = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    weather_conditions = models.CharField(max_length=100, blank=True)
    road_conditions = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    ai_detected = models.BooleanField(default=False)
    emergency_notified = models.BooleanField(default=False)
    police_notified = models.BooleanField(default=False)
    ambulance_notified = models.BooleanField(default=False)
    reported_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'accidents'
        ordering = ['-reported_at']
        indexes = [
            models.Index(fields=['severity']),
            models.Index(fields=['status']),
            models.Index(fields=['vehicle', 'reported_at']),
        ]

    def __str__(self):
        return f"Accident: {self.vehicle.license_plate} - {self.severity}"

class AccidentImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    accident = models.ForeignKey(Accident, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='accident_images/')
    description = models.TextField(blank=True)
    is_ai_analyzed = models.BooleanField(default=False)
    ai_analysis = models.JSONField(default=dict, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'accident_images'

    def __str__(self):
        return f"Image: {self.accident.id}"

class AccidentVideo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    accident = models.ForeignKey(Accident, on_delete=models.CASCADE, related_name='videos')
    video = models.FileField(upload_to='accident_videos/')
    description = models.TextField(blank=True)
    duration_seconds = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'accident_videos'

    def __str__(self):
        return f"Video: {self.accident.id}"
