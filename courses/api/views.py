from rest_framework import generics
from courses.api.serializers import SubjectSerializer
from courses.models import Subject


class SubjectListView(generics.ListAPIView):
    queryset = Subject.objects.all()    # Conjunto de consultas base para recuperar objectos
    serializer_class = SubjectSerializer    # La clase para serializar objetos

class SubjectDetailView(generics.RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer