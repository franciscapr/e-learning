from rest_framework import serializers
from courses.models import Subject


# Serializador para el modelo de subject
class SubjectSerializer(serializers.ModelSerializer):
    total_courses = serializers.IntegerField()

    class Meta:
        model = Subject    # Especificamos el modelo a serializar
        fields = ['id', 'title', 'slug', 'total_courses']    # Especificamos los campos del modelos en el fields