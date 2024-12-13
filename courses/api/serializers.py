from rest_framework import serializers
from courses.models import Subject, Course, Module
from django.db.models import Count


# Serializador para el modelo de subject
class SubjectSerializer(serializers.ModelSerializer):
    total_courses = serializers.IntegerField()
    popular_courses = serializers.SerializerMethodField()

    def get_popular_courses(self, obj):
        courses = obj.courses.annotate(
            total_students=Count('students')
        ).order_by('total_students')[:3]
        return[
            f'{c.title} ({c.total_students})' for c in courses
        ]

    class Meta:
        model = Subject    # Especificamos el modelo a serializar
        fields = ['id',
                    'title',
                    'slug',
                    'total_courses',
                    'popular_courses'
                    ]    # Especificamos los campos del modelos en el fields



class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['order', 'title', 'description']



class CourseSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True)    # Indicamos que este campos es de solo lectura y que estamos serializando multiples objetos
    
    class Meta:
        model = Course
        fields = [
            'id',
            'subject',
            'title',
            'overview',
            'created',
            'owner',
            'modules'
        ]