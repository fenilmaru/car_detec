import uuid
from django.db import models
from django.conf import settings

class EmergencyContact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='emergency_contacts')
    name = models.CharField(max_length=200)
    relationship = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'emergency_contacts'

    def __str__(self):
        return f"{self.name} ({self.relationship})"

class SOSAlert(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('responding', 'Responding'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed'),
    ]
    TYPE_CHOICES = [
        ('accident', 'Accident'),
        ('medical', 'Medical Emergency'),
        ('breakdown', 'Vehicle Breakdown'),
        ('security', 'Security Threat'),
        ('fire', 'Fire'),
        ('other', 'Other'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey('vehicles.Vehicle', on_delete=models.CASCADE, related_name='sos_alerts')
    driver = models.ForeignKey('drivers.Driver', on_delete=models.SET_NULL, null=True)
    alert_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    location = models.CharField(max_length=500)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    description = models.TextField(blank=True)
    auto_triggered = models.BooleanField(default=False)
    manual_triggered = models.BooleanField(default=False)
    notified_contacts = models.BooleanField(default=False)
    notified_emergency_services = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sos_alerts'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['alert_type']),
        ]

    def __str__(self):
        return f"SOS: {self.alert_type} - {self.status}"

class EmergencyService(models.Model):
    SERVICE_TYPE = [
        ('ambulance', 'Ambulance'),
        ('police', 'Police'),
        ('fire', 'Fire Department'),
        ('hospital', 'Hospital'),
        ('tow_truck', 'Tow Truck'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPE)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField()
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'emergency_services'

    def __str__(self):
        return f"{self.name} ({self.service_type})"
