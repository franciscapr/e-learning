from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from .models import Course
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.views.generic.base import TemplateResponseMixin, View
from .forms import ModuleFormSet


class OwnerMixin():
    def get_queryset(self):    
        qs = super().get_queryset()    # Utilizamos el mètodo get_queryset(), para obtener el queryset base.
        return qs.filter(owner=self.request.user)    # Recuperamos solo objetos que pertenecen al usuario actual.
    
class OwnerEditMixin:
    def form_valid(self, form):    # Implementamos el mètodo form_valid() cuando el formulario enviado es vàlido.
        form.instance.owner = self.request.user    # Guardamos la instancia (en formularios de modelo) y redifirimos al usuario success_url
        return super().form_valid(form)
    
class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin, PermissionRequiredMixin):    # Hereda de OwnerMixin
    model = Course    # El modelo utilizado para los QuerySet.
    fields = ['subject', 'title', 'slug', 'overview']    # Los campos del modeloq ue se usaràn para cosntruir el formulario de modelos en CreateView y UpdateViee
    success_url = reverse_lazy('manage_course_list')    # Usado por CreteView, UpdateView, DeleteView para redirigir al usuario desuès de enviar correctamente el formulario o eliminar un objeto.

class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    template_name = 'courses/manage/course/form.html'    # La plantilla que utilizaremos en las vistas de CreateView y UpdateView



# **** VISTAS QUE HEREDAN DE OwnerCourseMixin ****

class ManageCourseListView(OwnerCourseMixin, ListView):    # Lista los cursos creados porl usuario.
    model = Course
    template_name = 'courses/manage/course/list.html'    # Plantilla que lista los cursos.
    permission_required = 'courses.view_course'

class CourseCreateView(OwnerCourseEditMixin, CreateView):    # Usa un formulario de modelo para crear un nuevo objeto Course.
    permission_required = 'courses.add_course'

class CourseUpdateView(OwnerCourseEditMixin, UpdateView):    # Permite editar un objeto Course.
    permission_required = 'courses.change_course'

class CourseDeleteView(OwnerCourseMixin, DeleteView):    # Permite eliminar un objeto Course.
    template_name = 'courses/manage/course/delete.html'    # Plantilla para confirmar la eliminaciòn del curso.
    permission_required = 'courses.delete_course'


class CourseModuleUpdateView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/formset.html'
    course = None

    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course, data=data)
    
    def dispatch(self, request, pk):
        self.course = get_object_or_404(
            Course, id=pk, owner=request.user
        )
        return super().dispatch(request, pk)
    
    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response(
            {'course': self.course, 'formset': formset}
        )
    
    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response(
            {'course': self.course, 'formset': formset}
        )