import uuid
from django.db import models
from django.conf import settings

class Driver(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('inactive', 'Inactive'),
        ('on_leave', 'On Leave'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='driver_profile')
    license_number = models.CharField(max_length=50, unique=True)
    license_class = models.CharField(max_length=10, choices=[
        ('A', 'Class A'), ('B', 'Class B'), ('C', 'Class C'),
        ('D', 'Class D'), ('CDL', 'Commercial')
    ])
    license_issue_date = models.DateField()
    license_expiry_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    total_trips = models.PositiveIntegerField(default=0)
    total_distance_km = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    safety_score = models.DecimalField(max_digits=5, decimal_places=2, default=100.00)
    last_trip_date = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='driver_photos/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'drivers'
        ordering = ['-created_at']
        indexes = [models.Index(fields=['license_number']), models.Index(fields=['status'])]

    def __str__(self):
        return f"{self.user.username} - {self.license_number}"

class DriverHealth(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='health_records')
    blood_pressure = models.CharField(max_length=20, blank=True)
    heart_rate = models.PositiveIntegerField(null=True, blank=True)
    vision_test = models.BooleanField(null=True, blank=True)
    last_checkup = models.DateField(null=True, blank=True)
    medical_conditions = models.TextField(blank=True)
    medications = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'driver_health'
        ordering = ['-recorded_at']

    def __str__(self):
        return f"Health: {self.driver} - {self.recorded_at.date()}"
