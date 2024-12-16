from django.db import models
from django.conf import settings

class Message(models.Model):
    user = models.ForeignKey(    # EL user que escribio el mensaje
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,   # Un objeto user no puede ser eliminado si existen mensaes relacionados
        related_name='chat_messages'
    )
    course = models.ForeignKey(    # Cada mensaje pertenece a la sala de chat de un curso.
        'courses.Course',
        on_delete=models.PROTECT,    # Un objeto course no puede ser eliminado si existen mensajes relacionados
        related_name='chat_messages'
    )
    content = models.TextField()    # Almacenamos el contenido del mensaje
    send_on = models.DateTimeField(auto_now_add=True)    # Para almacenar la fecha y la hora en que el objeto del mensaje se guarda por primera vez

    def __str__(self):
        return f'{self.user} on {self.course} at {self.sent_on}'

