from django.forms.models import inlineformset_factory
from .models import Course, Module

ModuleFormSet = inlineformset_factory(
    Course,
    Module,
    fields=['title', 'description'],    # Campos que se incluiran en cada formset.
    extra=2,    # Permite establecer el nùmero de formularios vacios adicionales que se mostraràn en el formset.
    can_delete=True    # Permite marcar los objetos que se desean eliminar.
)