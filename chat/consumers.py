
from asgiref.sync import sync_to_async

# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from a_users.models import User
from .models import RoomChat, GroopRooms , MessageChat # Import RoomChat and GroopRooms models
# chat/consumers.py

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Get the user from the scope (assuming the user is authenticated)
        user = self.scope.get('user', None)

        if user.is_authenticated:
            # Fetch the room object using the room name (assumed to be a slug or identifier)
            try:
                room = await self.get_room(self.room_name)
                if room:
                    # Save the message to the RoomChat model
                    await self.save_message(user, room, message)
                else:
                    await self.send(text_data=json.dumps({
                        'message': 'Room does not exist.'
                    }))
            except GroopRooms.DoesNotExist:
                await self.send(text_data=json.dumps({
                    'message': 'Room does not exist.'
                }))

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    # Helper to get room by name
    @sync_to_async
    def get_room(self, room_name):
        return GroopRooms.objects.get(name=room_name)

    # Helper to save message to RoomChat
    @sync_to_async
    def save_message(self, user, room, message):
        RoomChat.objects.create(user=user, room=room, message=message)
