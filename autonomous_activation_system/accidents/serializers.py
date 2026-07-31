from rest_framework import serializers
from accidents.models import Accident, AccidentImage, AccidentVideo

class AccidentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccidentImage
        fields = '__all__'
        read_only_fields = ['id', 'uploaded_at']

class AccidentVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccidentVideo
        fields = '__all__'

class AccidentSerializer(serializers.ModelSerializer):
    vehicle_plate = serializers.CharField(source='vehicle.license_plate', read_only=True)
    driver_name = serializers.CharField(source='driver.user.username', read_only=True)
    image_count = serializers.SerializerMethodField()

    class Meta:
        model = Accident
        fields = '__all__'

    def get_image_count(self, obj):
        return obj.images.count()
