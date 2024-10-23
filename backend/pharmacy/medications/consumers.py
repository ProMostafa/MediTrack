import json
from channels.generic.websocket import AsyncWebsocketConsumer

class RefillConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'refill_updates'

        # Join the group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)

        # Broadcast refill update to the group
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'refill_status_update',
                'message': data['message']
            }
        )

    # Handle broadcast
    async def refill_status_update(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
