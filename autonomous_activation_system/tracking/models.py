import uuid
from django.db import models

class GPSLocation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey('vehicles.Vehicle', on_delete=models.CASCADE, related_name='gps_locations')
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    altitude = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    speed = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    heading = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    accuracy = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    battery_level = models.PositiveIntegerField(null=True, blank=True)
    ignition_on = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'gps_locations'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['vehicle', 'timestamp']),
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return f"GPS: {self.vehicle.license_plate} @ {self.timestamp}"

class RouteHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey('vehicles.Vehicle', on_delete=models.CASCADE, related_name='route_histories')
    trip = models.ForeignKey('vehicles.Trip', on_delete=models.SET_NULL, null=True, related_name='route_history')
    start_latitude = models.DecimalField(max_digits=10, decimal_places=7)
    start_longitude = models.DecimalField(max_digits=10, decimal_places=7)
    end_latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    end_longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    total_distance_km = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    avg_speed = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    max_speed = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'route_history'
        ordering = ['-start_time']

    def __str__(self):
        return f"Route: {self.vehicle.license_plate} - {self.start_time.date()}"
