from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = 'chat'  # Group name (you can use any name)
        self.room_group_name = 'chat_group_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Broadcast the received message to all connected clients in the group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'username': self.scope['user'].username,
                'message': message
            }
        )

    def chat_message(self, event):
        # Send the received chat message to the WebSocket
        username = event['username']
        message = event['message']
        self.send(text_data=json.dumps({
            'username': username,
            'message': message
        }))
