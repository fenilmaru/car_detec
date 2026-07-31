from rest_framework import generics, permissions, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count, Avg, Q
from django.utils import timezone
from datetime import timedelta

# Vehicles
from vehicles.models import Vehicle, VehicleType, Trip, TripRoute
from vehicles.serializers import VehicleSerializer, VehicleTypeSerializer, TripSerializer

# Drivers
from drivers.models import Driver, DriverHealth
from drivers.serializers import DriverSerializer, DriverHealthSerializer

# Accidents
from accidents.models import Accident, AccidentImage, AccidentVideo
from accidents.serializers import AccidentSerializer, AccidentImageSerializer

# Camera & Detections
from camera.models import Camera, DetectionLog
from camera.serializers import CameraSerializer, DetectionLogSerializer

# Tracking
from tracking.models import GPSLocation, RouteHistory
from tracking.serializers import GPSLocationSerializer, RouteHistorySerializer

# Emergency
from emergency.models import SOSAlert, EmergencyContact, EmergencyService
from emergency.serializers import SOSAlertSerializer, EmergencyContactSerializer, EmergencyServiceSerializer

# Notifications
from notifications.models import Notification
from notifications.serializers import NotificationSerializer


# Pagination
class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


# Vehicle API
class VehicleListCreateAPI(generics.ListCreateAPIView):
    queryset = Vehicle.objects.select_related('vehicle_type', 'owner').all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination
    search_fields = ['license_plate', 'make', 'model', 'vin']

    def get_queryset(self):
        qs = super().get_queryset()
        status = self.request.query_params.get('status')
        if status:
            qs = qs.filter(status=status)
        return qs


class VehicleDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vehicle.objects.select_related('vehicle_type', 'owner').all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated]


class VehicleTypeListAPI(generics.ListAPIView):
    queryset = VehicleType.objects.filter(is_active=True)
    serializer_class = VehicleTypeSerializer
    permission_classes = [IsAuthenticated]


# Driver API
class DriverListCreateAPI(generics.ListCreateAPIView):
    queryset = Driver.objects.select_related('user').all()
    serializer_class = DriverSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination
    search_fields = ['license_number', 'user__username', 'user__email']


class DriverDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Driver.objects.select_related('user').all()
    serializer_class = DriverSerializer
    permission_classes = [IsAuthenticated]


# Trip API
class TripListCreateAPI(generics.ListCreateAPIView):
    queryset = Trip.objects.select_related('vehicle', 'driver').all()
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination
    search_fields = ['vehicle__license_plate']

    def get_queryset(self):
        qs = super().get_queryset()
        status = self.request.query_params.get('status')
        if status:
            qs = qs.filter(status=status)
        return qs


class TripDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trip.objects.select_related('vehicle', 'driver').all()
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated]


# Accident API
class AccidentListCreateAPI(generics.ListCreateAPIView):
    queryset = Accident.objects.select_related('vehicle', 'driver').all()
    serializer_class = AccidentSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination


class AccidentDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Accident.objects.select_related('vehicle', 'driver').all()
    serializer_class = AccidentSerializer
    permission_classes = [IsAuthenticated]


# Camera API
class CameraListCreateAPI(generics.ListCreateAPIView):
    queryset = Camera.objects.select_related('vehicle').all()
    serializer_class = CameraSerializer
    permission_classes = [IsAuthenticated]


class CameraDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Camera.objects.select_related('vehicle').all()
    serializer_class = CameraSerializer
    permission_classes = [IsAuthenticated]


# Detection Log API
class DetectionLogListAPI(generics.ListAPIView):
    queryset = DetectionLog.objects.select_related('vehicle', 'camera').order_by('-created_at')
    serializer_class = DetectionLogSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination

    def get_queryset(self):
        qs = super().get_queryset()
        dtype = self.request.query_params.get('type')
        severity = self.request.query_params.get('severity')
        vehicle = self.request.query_params.get('vehicle')
        if dtype:
            qs = qs.filter(detection_type=dtype)
        if severity:
            qs = qs.filter(severity=severity)
        if vehicle:
            qs = qs.filter(vehicle__license_plate=vehicle)
        return qs


# GPS API
class GPSLocationListAPI(generics.ListAPIView):
    serializer_class = GPSLocationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        vehicle = self.request.query_params.get('vehicle')
        qs = GPSLocation.objects.select_related('vehicle')
        if vehicle:
            qs = qs.filter(vehicle__license_plate=vehicle)
        return qs.order_by('-timestamp')[:100]


# Emergency API
class SOSAlertListCreateAPI(generics.ListCreateAPIView):
    queryset = SOSAlert.objects.select_related('vehicle', 'driver').all()
    serializer_class = SOSAlertSerializer
    permission_classes = [IsAuthenticated]


class SOSAlertDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = SOSAlert.objects.select_related('vehicle', 'driver').all()
    serializer_class = SOSAlertSerializer
    permission_classes = [IsAuthenticated]


class EmergencyServiceListAPI(generics.ListAPIView):
    queryset = EmergencyService.objects.filter(is_active=True)
    serializer_class = EmergencyServiceSerializer
    permission_classes = [IsAuthenticated]


# Notification API
class NotificationListAPI(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.notifications.order_by('-created_at')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_notification_read(request, pk):
    try:
        notif = request.user.notifications.get(pk=pk)
        notif.is_read = True
        notif.save()
        return Response({'status': 'marked as read'})
    except Notification.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)


# Analytics API
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def analytics_overview(request):
    now = timezone.now()
    thirty = now - timedelta(days=30)
    seven = now - timedelta(days=7)

    total_vehicles = Vehicle.objects.count()
    active_vehicles = Vehicle.objects.filter(status='active').count()
    total_drivers = Driver.objects.filter(status='active').count()
    total_accidents = Accident.objects.count()
    recent_accidents = Accident.objects.filter(reported_at__gte=seven).count()
    active_sos = SOSAlert.objects.filter(status='active').count()
    total_detections = DetectionLog.objects.filter(created_at__gte=thirty).count()

    detections_by_type = list(DetectionLog.objects.filter(created_at__gte=thirty).values('detection_type').annotate(count=Count('id')))
    accidents_by_severity = list(Accident.objects.filter(reported_at__gte=thirty).values('severity').annotate(count=Count('id')))

    return Response({
        'total_vehicles': total_vehicles,
        'active_vehicles': active_vehicles,
        'active_drivers': total_drivers,
        'total_accidents': total_accidents,
        'recent_accidents': recent_accidents,
        'active_sos_alerts': active_sos,
        'total_detections_30d': total_detections,
        'detections_by_type': detections_by_type,
        'accidents_by_severity': accidents_by_severity,
    })


# Reports API
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_report(request):
    period = request.query_params.get('period', 'week')
    if period == 'day':
        start = timezone.now() - timedelta(days=1)
    elif period == 'month':
        start = timezone.now() - timedelta(days=30)
    elif period == 'year':
        start = timezone.now() - timedelta(days=365)
    else:
        start = timezone.now() - timedelta(days=7)

    trips = Trip.objects.filter(start_time__gte=start).count()
    accidents = Accident.objects.filter(reported_at__gte=start).count()
    detections = DetectionLog.objects.filter(created_at__gte=start).count()
    avg_confidence = DetectionLog.objects.filter(created_at__gte=start).aggregate(avg=Avg('confidence_score'))['avg']

    return Response({
        'period': period,
        'start_date': start.isoformat(),
        'total_trips': trips,
        'total_accidents': accidents,
        'total_detections': detections,
        'avg_detection_confidence': round(float(avg_confidence or 0), 4),
        'generated_at': timezone.now().isoformat(),
    })
