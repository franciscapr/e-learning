from django.contrib.auth.models import User
from django.db import models


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

    def __str__(self):
        return self.title