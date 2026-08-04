from rest_framework import serializers
from autonomous_activation_system.tracking.models import GPSLocation, RouteHistory

class GPSLocationSerializer(serializers.ModelSerializer):
    vehicle_plate = serializers.CharField(source='vehicle.license_plate', read_only=True)

    class Meta:
        model = GPSLocation
        fields = '__all__'

class RouteHistorySerializer(serializers.ModelSerializer):
    vehicle_plate = serializers.CharField(source='vehicle.license_plate', read_only=True)

    class Meta:
        model = RouteHistory
        fields = '__all__'
