from rest_framework import generics
from courses.api.serializers import SubjectSerializer
from courses.models import Subject, Course
from django.db.models import Count
from courses.api.pagination import StandardPagination
from rest_framework import viewsets
from courses.api.serializers import CourseSerializer, SubjectSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from courses.api.permissions import IsEnrolled
from courses.api.serializers import CourseWithContentsSerializer

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
    @action(    # Especificamos que esta es una acciòn que se realiza sobre un solo objeto.
        detail=True,
        methods=['post'],    # Solo se permite el mètodo post
        authentication_classes=[BasicAuthentication],    # Establecemos las clases de autenticaciò
        permission_classes=[IsAuthenticated]    # y permisos
    )
    def enroll(self, request, *args, **kwargs):
        course = self.get_object()    # Recuperamos el objeto course
        course.students.add(request.user)
        return Response({'enrolled': True})
    
    @action(    # Especificamos que esta acciòn se debe realizar sobre solo un objeto.
        detail=True,
        methods=['get'],    # Especificamos que solo se permite el mètodo GET para esta acciòn.
        serializer_class=CourseWithContentsSerializer,    # Utilizamos la clase CourseWithContentsSerializer que incluye los contenidos del curso serializados.
        authentication_classes=[BasicAuthentication],    # Utilizamos estos permisos para asegurarnos de que solo los usuarios inscritos en los cursos puedan acceder a su contenido.
        permission_classes=[IsAuthenticated, IsEnrolled]
    )
    
    def contents(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)    # Utilizamos el retriver() existente para devolver el objeto del curso.







# class CourseEnrollView(APIView):
#     authentication_classes = [BasicAuthentication]
#     permission_classes = [IsAuthenticated]    # Evitamos que los usuarios anonimos ingresen a las vistas

#     def post(self, request, pk, format=None):
#         course = get_object_or_404(Course, pk=pk)
#         course.students.add(request.user)
#         return Response({'enrolled': True})