import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

# Consumidor
class ChatConsumer(WebsocketConsumer):
    def connect(self):    # Mètodo connect(), se llama cuandos e recibe una nueva conexiòn
        self.id = self.scope['url_route']['kwargs']['course_id']    # Recuperamos el parametro coruse_id de la url. cada consumidor tiene un scope con infromaciòn sobre su conexiòn.
        self.room_group_name = f'chat_{self.id}'
        # join room group
        async_to_sync(self.channel_layer.group_add)(   # Utilizamos el mètodo group_add de la capa de canales para añadir el canal al grupo.
            self.room_group_name, self.channel_name    # usamos async_to_sync() para poder llamar al mètodo asincrono de la capa de canales.
        )   
        
        # Mantenemos la llamada self.accepts() para aceptar la conexiòn al WebSocket
        self.accept()

    def diconnect(self, close_code):    # Se llama disconnect() cuando el socket se cierra. Utilizamos pass poruqe no necesitamos implementar ninguna acciòn cuando un cliente cierra la conexiòn.
        # leave rom groip
        async_to_sync(self.channel_layer.group_discard)(    # Cuando la conexiòn se cierra, llamamos al mètodo group_discard() de la capa de canales para salir del grupo.
            self.room_group_name, self.channel_name    # Usamo el envoltorio async_to_sync() para poder llamar al mètodo asincrònico de la capa de canales
        )

    # receive message from WebSocket

    def receive(self, text_data):    # Se llama cada vez que se recibe un datos desde el WebSocket. Se espera que los datos sean texto recibido como text_data. Tratamos los datos de texto recibidos como JSON
        text_data_json = json.loads(text_data)
        message = text_data_json['message']    # Utilizamos json.loads() para cargar los datos JSON recibidos en un diccionario de Python.
        # send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',    # EL tipo de evento, esta es una clave especial que corresponde al nombre del mètodo que debe ser invocado en los consumidores que reciben el evento.
                'message': message,    # Mensaje real que se esta enviando.
            }
        )

    def chat_message(self, event):    # Cuando un mensaje con el tupo chat_message se envia al grupo, todos los consumidores suscritos al grupo recibiran el mensaje y ajecutaràn el mètpdp chat_message()
        # send message to WebSocket
        self.send(text_data=json.dumps(event))