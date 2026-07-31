from rest_framework import serializers
from autonomous_activation_system.notifications.models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    vehicle_plate = serializers.CharField(source='vehicle.license_plate', read_only=True)

    class Meta:
        model = Notification
        fields = '__all__'
