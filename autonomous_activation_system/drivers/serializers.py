from rest_framework import serializers
from autonomous_activation_system.drivers.models import Driver, DriverHealth

class DriverSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    phone = serializers.CharField(source='user.phone', read_only=True)

    class Meta:
        model = Driver
        fields = '__all__'

class DriverHealthSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverHealth
        fields = '__all__'
