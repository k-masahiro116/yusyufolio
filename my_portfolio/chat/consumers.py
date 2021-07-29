from channels.exceptions import StopConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
import collections
import json

class ChatConsumer(AsyncWebsocketConsumer):
    
    def __init__(self, *args, **kwargs):
        super(ChatConsumer, self).__init__(*args, **kwargs)
        self.handler_tasks = collections.defaultdict(list)
        self.joined_groups = set()

        self.room_name = None
        self.room_group_name = None
        
    async def join_group(self, group_name):
        await self.channel_layer.group_add(
            group_name, self.channel_name
        )
        self.joined_groups.add(group_name)
    
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']

        self.room_group_name = 'chat_{}'.format(self.room_name)
        print("group_name: ", self.room_group_name)

        # Join room group
        await self.join_group(self.room_group_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.close()
        self.joined_groups.clear()
        print(self.room_group_name, self.channel_name)

        raise StopConsumer()

    async def receive(self, text_data, **kwargs):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

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