from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from autonomous_activation_system.vehicles.models import Vehicle
from autonomous_activation_system.tracking.models import GPSLocation
from autonomous_activation_system.camera.models import DetectionLog
from autonomous_activation_system.accidents.models import Accident
from autonomous_activation_system.emergency.models import SOSAlert
from autonomous_activation_system.notifications.models import Notification
from django.utils import timezone

class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'dashboard'
        self.room_group_name = f'dashboard_{self.room_name}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'get_stats':
            stats = await self.get_dashboard_stats()
            await self.send(text_data=json.dumps(stats))

    async def dashboard_update(self, event):
        await self.send(text_data=json.dumps(event['data']))

    @database_sync_to_async
    def get_dashboard_stats(self):
        return {
            'type': 'dashboard_stats',
            'total_vehicles': Vehicle.objects.count(),
            'active_vehicles': Vehicle.objects.filter(status='active').count(),
            'total_accidents': Accident.objects.count(),
            'active_sos': SOSAlert.objects.filter(status='active').count(),
            'pending_notifications': Notification.objects.filter(is_read=False).count(),
        }


class GPSConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.vehicle_id = self.scope['url_route']['kwargs'].get('vehicle_id', 'all')
        self.room_group_name = f'gps_{self.vehicle_id}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def gps_update(self, event):
        await self.send(text_data=json.dumps(event['data']))

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data.get('action') == 'send_location':
            await self.save_location(data)

    @database_sync_to_async
    def save_location(self, data):
        try:
            vehicle = Vehicle.objects.get(id=data['vehicle_id'])
            loc = GPSLocation.objects.create(
                vehicle=vehicle,
                latitude=data['latitude'],
                longitude=data['longitude'],
                speed=data.get('speed', 0),
            )
            return {'status': 'saved', 'id': str(loc.id)}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}


class DetectionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'detections'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def detection_update(self, event):
        await self.send(text_data=json.dumps(event['data']))


class EmergencyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'emergency'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def emergency_alert(self, event):
        await self.send(text_data=json.dumps(event['data']))
