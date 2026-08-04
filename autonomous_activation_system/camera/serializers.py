from rest_framework import serializers
from autonomous_activation_system.camera.models import Camera, DetectionLog

class CameraSerializer(serializers.ModelSerializer):
    vehicle_plate = serializers.CharField(source='vehicle.license_plate', read_only=True)

    class Meta:
        model = Camera
        fields = '__all__'

class DetectionLogSerializer(serializers.ModelSerializer):
    vehicle_plate = serializers.CharField(source='vehicle.license_plate', read_only=True)
    camera_name = serializers.CharField(source='camera.name', read_only=True)

    class Meta:
        model = DetectionLog
        fields = '__all__'
