from django.contrib.auth.models import User
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from .fields import OrderField


# Subjeto
class Subject(models.Model):    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title
    
# Curso
class Course(models.Model):
    owner = models.ForeignKey(    # Instructor que creò el curso
        User,
        related_name='courses_created',
        on_delete=models.CASCADE
    )
    subject = models.ForeignKey(    # Materia a la que pertenece este curso
        Subject,
        related_name='courses',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)    # Titulo del curso
    slug = models.SlugField(max_length=200, unique=True)    # Slug del curso ---> Para las URL
    overview = models.TextField()    # UNa columna de tipo text para almacenar una descripciòn general del curos
    created = models.DateTimeField(auto_now_add=True)    # Fecha y hora en la que se creo el curso
    students = models.ManyToManyField(
        User,
        related_name='courses_joined',
        blank=True
    )

    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.title
    
# Modulo
class Module(models.Model):
    course = models.ForeignKey(
        Course, related_name='modules', on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])    # nmbramo el nuevo campo order y especificamos que el orden se calcula con respuesta el curso al establecer for_fiedls=['course]

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.order}. {self.title}'
    
    

# Modelo de Contenido
class Content(models.Model):
    module = models.ForeignKey(    # Apuntamos el modelo de modula ya que este es el que contenie mùltiples contenidos
        Module,
        related_name='contents',
        on_delete= models.CASCADE
    )
    content_type = models.ForeignKey(    # Campo ForeignKey al modelo ContentType
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to = {    # Limitamos los objetos ContentType que se pueden usar para la relaciòn generica
            'model__in': ('text', 'video', 'image', 'file')    # Utilizamos la bùesqueda de campo model__in para filtrar la consulta a los objetos ContenType cuyo atributo models sea 'text', 'video0, 'image', 'file'.
        }
    )
    object_id = models.PositiveIntegerField()    # Alamacenamos la llave primaria del objeto relacionado
    item = GenericForeignKey('content_type', 'object_id')    # Compo GenericForeignKey para el objeto relacionado que combina los dos campos anteriores
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']



# Modelo Abstracto
class ItemBase(models.Model):
    owner = models.ForeignKey(User,    # Usuario que creo el contenido
                              related_name='%(class)s_relared',    # related_name diferentes para cada submodelo
                              on_delete=models.CASCADE
                              )
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
    
    def __str__(self):
        return self.title
    
class Text(ItemBase):    # Almacenamos contenido de texto
    content = models.TextField()

class File(ItemBase):    # Para almacenar archivos, como pdfs
    file = models.FileField(upload_to='files')

class Image(ItemBase):    # Para almacenar archivos de imagenes
    file = models.FileField(upload_to='images')

class Video(ItemBase):    # Para almacenar videos, utilizamos urlfiled para proporcionar una url de video con el fin de incrustarlo
    url = models.URLField()