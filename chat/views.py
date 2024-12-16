from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from courses.models import Course

# Usamos @login_required para evitar que cualquier usuario no autenticado acceda a la vista.
@login_required
def course_chat_room(request, course_id):    # Recibe el paràmetro obligatorio course_id para recuperar el curso con el id proporcionado.
    try:
        # retrieve course with given id joined by the current user
        course = request.user.courses_joined.get(id=course_id)    # Recuperamos los cursos en los cuales el usuario esta inscrito.
    except Course.DoesNotExist:    # SI el curso con el id dado no existe o el usuario no esta inscrito se devuelve HttpResponseForbidden que se traduce como uan respuesta http 403
        # user is not studnet of the course or course does not exist
        return HttpResponseForbidden()
    # retrive chat history
    latest_messages = course.chat_messages.select_related(
        'user'
    ).order_by('-id'[:5])
    latest_messages = reversed(latest_messages)    
    return render(request,
                   'chat/room.html',
                    {'course': course, 'latest_messages': latest_messages})    # Si el curso con el ID dado si existe y el usuario esta inscrito en el , se renderiza la plantilla chat/room.html