from rest_framework import generics
from courses.api.serializers import SubjectSerializer
from courses.models import Subject, Course
from django.db.models import Count
from courses.api.pagination import StandardPagination
from rest_framework import viewsets
from courses.api.serializers import CourseSerializer, SubjectSerializer


# class SubjectListView(generics.ListAPIView):
#     queryset = Subject.objects.annotate(total_courses=Count('courses'))     # Conjunto de consultas base para recuperar objectos - anotamos el conteo de cursos relacionados
#     serializer_class = SubjectSerializer    # La clase para serializar objetos
#     pagination_class = StandardPagination

# class SubjectDetailView(generics.RetrieveAPIView):
#     queryset = Subject.objects.annotate(total_courses=Count('courses'))
#     serializer_class = SubjectSerializer

class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Subject.objects.annotate(total_courses=Count('courses'))
    serializer_class = SubjectSerializer
    pagination_class = StandardPagination

class CourseViewSet(viewsets.ReadOnlyModelViewSet):    # Acciones de solo lectura
    queryset = Course.objects.prefetch_related('modules')    # Obtenemos los objetos de module
    serializer_class = CourseSerializer
    pagination_class = StandardPagination