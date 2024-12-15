import json
from channels.generic.websocket import WebsocketConsumer

# Consumidor
class ChatConsumer(WebsocketConsumer):
    def connect(self):    # Mètodo connect(), se llama cuandos e recibe una nueva conexiòn
        # accept connection
        self.accept()

    def diconnect(self, close_code):    # Se llama disconnect() cuando el socket se cierra. Utilizamos pass poruqe no necesitamos implementar ninguna acciòn cuando un cliente cierra la conexiòn.
        pass
    # receive message from WebSocket

    def receive(self, text_data):    # Se llama cada vez que se recibe un datos desde el WebSocket. Se espera que los datos sean texto recibido como text_data. Tratamos los datos de texto recibidos como JSON
        text_data_json = json.loads(text_data)
        message = text_data_json['message']    # Utilizamos json.loads() para cargar los datos JSON recibidos en un diccionario de Python.
        # send message to WebSocket
        self.send(text_data=json.dumps({'message': message}))