"""
WebSocket Consumers for real-time features.
"""
import json
from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    """Real-time notifications via WebSocket."""
    
    async def connect(self):
        self.user = self.scope.get('user')
        if self.user and self.user.is_authenticated:
            self.group = f'user_{self.user.id}'
            await self.channel_layer.group_add(self.group, self.channel_name)
            await self.accept()
        else:
            await self.close()
    
    async def disconnect(self, close_code):
        if hasattr(self, 'group'):
            await self.channel_layer.group_discard(self.group, self.channel_name)
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        command = data.get('command')
        if command == 'ping':
            await self.send({'type': 'pong'})
        elif command == 'subscribe':
            course_id = data.get('course_id')
            group = f'course_{course_id}'
            await self.channel_layer.group_add(group, self.channel_name)
            await self.send({'type': 'subscribed', 'course_id': course_id})
    
    async def notification_message(self, event):
        await self.send(text_data=json.dumps(event['message']))


class ChatConsumer(AsyncWebsocketConsumer):
    """Real-time chat."""
    
    async def connect(self):
        query = self.scope.get('query_string', b'').decode()
        self.room_name = None
        for param in query.split('&'):
            if param.startswith('room='):
                self.room_name = param[5:]
                break
        
        if self.room_name:
            self.room_group = f'chat_{self.room_name}'
            await self.channel_layer.group_add(self.room_group, self.channel_name)
            await self.accept()
        else:
            await self.close()
    
    async def disconnect(self, close_code):
        if hasattr(self, 'room_group'):
            await self.channel_layer.group_discard(self.room_group, self.channel_name)
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message', '')
        sender = self.scope.get('user', {}).get('email', 'anonymous')
        await self.channel_layer.group_send(self.room_group, {
            'type': 'chat_message',
            'message': message,
            'sender': sender
        })
    
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': event['message'],
            'sender': event['sender']
        }))


class AttendanceConsumer(AsyncWebsocketConsumer):
    """Real-time attendance QR sessions."""
    
    async def connect(self):
        self.session_active = False
        await self.accept()
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        cmd = data.get('command')
        
        if cmd == 'start_session':
            self.session_active = True
            await self.send(text_data=json.dumps({'type': 'session_started', 'token': data.get('token')}))
        elif cmd == 'end_session':
            self.session_active = False
            await self.send(text_data=json.dumps({'type': 'session_ended'}))
        elif cmd == 'scan' and self.session_active:
            await self.send(text_data=json.dumps({'type': 'scan_result', 'student': data.get('student'), 'success': True}))
