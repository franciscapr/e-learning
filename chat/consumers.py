import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.utils import timezone
from chat.models import Message

# Consumidor
class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):    # Mètodo connect(), se llama cuandos e recibe una nueva conexiòn
        self.user = self.scope['user']
        self.id = self.scope['url_route']['kwargs']['course_id']    # Recuperamos el parametro coruse_id de la url. cada consumidor tiene un scope con infromaciòn sobre su conexiòn.
        self.room_group_name = f'chat_%s' % self.id
        # join room group
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        # accept connection
        await self.accept()    # await para realizar operaciones asincronas

    
    async def disconnect(self, close_code):
        # leave room group
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    async def persist_message(self, message):    # Tomamos como parametro message y crea un objeto message en la base de datos con el mensaje proporcionado, el usuario autenticado relacionado y el id del objeto course al que pertenece la sala del chat del grupo.
        # send message to websocket
        await Message.objects.acreate(
            user=self.user, course_id=self.id, content=message
        )


    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']    # Utilizamos json.loads() para cargar los datos JSON recibidos en un diccionario de Python.
        now = timezone.now()
        # send message to room group

        await self.channel_layer.group_send(
        self.room_group_name,
        {
            'type': 'chat_message',    # EL tipo de evento, esta es una clave especial que corresponde al nombre del mètodo que debe ser invocado en los consumidores que reciben el evento.
            'message': message,    # Mensaje real que se esta enviando.
            'user': self.user.username,
            'datetime': now.isoformat(),
        },
        )
        # persist message
        await self.persist_message(message)
        
    async def chat_message(self, event):
        # sedn message to WebSocket
        await self.send(text_data=json.dumps(event))