# chat/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from django.contrib.auth.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user_id = self.scope["session"]["_auth_user_id"]
        self.group_name = "{}".format(user_id)
#         Join room group
        user = self.scope['user']
        self.update_user_status(user, 'online')
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name,

        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        user = self.scope['user']
        self.update_user_status(user, 'offline')
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name,

        )
        user = self.scope['user']

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):

        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'recieve_group_message',
                'message': message,

            }

        )

    async def recieve_group_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(
            text_data=json.dumps({
                'message': message
            }))

    @database_sync_to_async
    def update_user_status(self, user, status):
        """
        Updates the user `status.
        `status` can be one of the following status: 'online', 'offline' or 'away'
        """
        return User.objects.filter(pk=user.pk).update(status=status)
