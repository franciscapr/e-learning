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
from django.apps import apps
from django.forms.models import modelform_factory
from .models import Module, Content

from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.db.models import Count
from .models import Subject
from django.views.generic.detail import DetailView
from students.forms import CourseEnrollForm


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
    

class ContentCreateUpdateView(TemplateResponseMixin, View):
    module = None
    model = None
    obj = None
    template_name = 'courses/manage/content/form.html'

    def get_model(self, model_name):
        if model_name in ['text', 'video', 'image', 'file']:    # Verificamos que el nombre del modelo proporcionado sea uno de los cuatro modelos de contenid: text, video, image o file
            return apps.get_model(    # Utilizamos el mòdulo apps de django para obtener la clase real corrspondiente al nombre del modelo.
                app_label='courses', model_name=model_name
            )
        return None    # SI el nombre del modelo proporcionado no es vàlido, devuelve None
    
    def get_form(self, model, *args, **kwargs):    # Csontruimos un formulario dinàmico
        Form = modelform_factory(
            model, exclude=['owner', 'order', 'created', 'updated']    # Utilizamos exclude para especificar los campos comunes que se deben excluir del formulario y permitir que todos los demàs atributos se incluyan automàticamente.
        )
        return Form(*args, **kwargs)
    
    def dispatch(self, request, module_id, model_name, id=None):
        self.module = get_object_or_404(
            Module, id=module_id, course__owner=request.user
        )
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(
                self.model, id=id, owner=request.user
            )
        return super().dispatch(request, module_id, model_name, id)
        
    def get(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response(
            {'form': form, 'object': self.obj}
        )
    
    def post(self, request, module_id, model_name, id=None):
        form = self.get_form(
            self.model,
            instance = self.obj,
            data = request.POST,
            files = request.FILES
        )
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                # New content
                Content.objects.create(module=self.module, item=obj)
            return redirect('module_content_list', self.module.id)
        return self.render_to_response(
            {'form': form, 'object': self.obj}
        )
    
class ContentDeleteView(View):    # Recuperamos el objeto de contenido con el ID proporcionado
    def post(self, request, id):
        content = get_object_or_404(
            Content, id=id, module__course__owner=request.user
        )
        module = content.module
        content.item.delete()    # ELiminamos el objeto de contenido y redirige al usuario a la url module_content_list
        content.delete()
        return redirect('module_content_list', module.id)
    

class ModuleContentListView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/content_list.html'

    def get(self, request, module_id):
        module = get_object_or_404(
            Module, id=module_id, course__owner=request.user    # Obtenemos el objeto de Module con el ID proporcionado que pertenece al suaurio actual y renderiza una plantilla con al mòdulo dado.
        )
        return self.render_to_response({'module': module})
    

class ModuleOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):    # Actualizamos el orden de los mòdulos del curso
    def post(self, request):
        for id, order in self.request_json.items():
            Module.objects.filter(
                id=id, course__owner=request.user
            ).update(order=order)
        return self.render_json_response({'saved': 'OK'})
    
class ContentOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request):
        for id, order in self.request_json.items():
            Content.objects.filter(
                id=id, module__course__owner=request.user
            ).update(order=order)
        return self.render_json_response({'saved': 'OK'})
    
class CourseListView(TemplateResponseMixin, View):
    model = Course
    template_name = 'courses/course/list.html'

    def get(self, request, subject=None):
        subjects = Subject.objects.annotate(    # Recuperamos todas las asignaturas  
            total_courses = Count('courses')    # incluimos el nùmero total de crusos para cada asignatura
        )
        courses = Course.objects.annotate(
            total_modules=Count('modules')
        )
        if subject:
            subject = get_object_or_404(Subject, slug=subject)
            courses = courses.filter(subject=subject)
        return self.render_to_response(
                {
                    'subjects': subjects,
                    'subject': subject,
                    'courses': courses
                }
            )
        
class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enroll_form'] = CourseEnrollForm(
            initial={'course': self.object}
        )
        return context