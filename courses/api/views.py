from rest_framework import generics
from courses.api.serializers import SubjectSerializer
from courses.models import Subject
from django.db.models import Count
from courses.api.pagination import StandardPagination


class SubjectListView(generics.ListAPIView):
    queryset = Subject.objects.annotate(total_courses=Count('courses'))     # Conjunto de consultas base para recuperar objectos - anotamos el conteo de cursos relacionados
    serializer_class = SubjectSerializer    # La clase para serializar objetos
    pagination_class = StandardPagination

class SubjectDetailView(generics.RetrieveAPIView):
    queryset = Subject.objects.annotate(total_courses=Count('courses'))
    serializer_class = SubjectSerializer