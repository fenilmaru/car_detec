from rest_framework import serializers
from autonomous_activation_system.vehicles.models import Vehicle, VehicleType, Trip, TripRoute

class VehicleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleType
        fields = '__all__'

class VehicleSerializer(serializers.ModelSerializer):
    vehicle_type_name = serializers.CharField(source='vehicle_type.name', read_only=True)
    owner_name = serializers.CharField(source='owner.username', read_only=True)
    trip_count = serializers.SerializerMethodField()

    class Meta:
        model = Vehicle
        fields = '__all__'

    def get_trip_count(self, obj):
        return obj.trips.count()

class TripSerializer(serializers.ModelSerializer):
    vehicle_plate = serializers.CharField(source='vehicle.license_plate', read_only=True)
    driver_name = serializers.CharField(source='driver.user.username', read_only=True)

    class Meta:
        model = Trip
        fields = '__all__'

class TripRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripRoute
        fields = '__all__'
