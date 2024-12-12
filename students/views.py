from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from .forms import CourseEnrollForm

class StudentRegistrationView(CreateView):
    template_name = 'students/student/registration.html'    # Ruta de la plantilla para renderizar la vista.
    form_class = UserCreationForm    # Formulario para crear los objetos
    success_url = reverse_lazy('student_course_list')    # Url a la que se redirige el usuario cuando el formulario se envia correctamente.

    def form_valid(self, form):    # Se ejecuta la funciòn fomr_valid() cuando los datos del formulario son vàlidos y se han enviado. Este metodo devuelve una respuesta HTTP
        result = super().form_valif(form)
        cd = form.cleaned_data
        user = authenticate(
            username=cd['username'], password=cd['password1']
        )
        login(self.request, user)
        return result
    
class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy(
            'student_course_detail', args=[self.course.id]
        )