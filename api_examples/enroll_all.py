from decouple import config
import requests    # Importamos la biblioteca request

username = config('USERNAME')
password = config('PASSWORD')

base_url = 'http://127.0.0.1:8000/api/'     # Definimos una url base para la api 
# url = f'{base_url}courses/'    # url para el endpoint de la lista de cursos
# available_courses = []    # Definimos una lista vacia

# while url is not None:    # Usamos el bucle while para paginar sobre todas las pàginas de resultados.
#     print(f'Loading courses from {url}')
#     r = requests.get(url)    # Usamos requests.get() para recuperar datos de la API enviando una solicitad get a la url http://127.0.0.1:8000/api/courses/
#     response = r.json()    # Usamos el mètodo json() del objeto de respuesta para decodificar los datos JSON devueltos por la API.
#     url = response['next']    # Almacenamos el atributo next en la variable url para recuperar la siguiente pàgina de resultados en el bucle while.
#     courses = response['results']
#     available_courses += [course['title'] for course in courses]    # Agregamos e atributo title de cada curso a la lista available_courses.
# print(f'Available courses: {", ".join(available_courses)}')    # Cuando la variable url es None, llega a la ùltima pàgina de resultados y no recuperamos màs pàginas.
#     # Por ultimo imprimimos la lista de cursos disponibles.

# for course in courses:
#     course_id = course['id']
#     course_title = course['title']
#     r = requests.post(
#         f'{base_url}courses/{course_id}/enroll/',
#         auth=(username, password)
#     )
#     if r.status_code == 200:
#         # successful request
#         print(f'Successfully wnrolled in {course_title}')

url = f'{base_url}courses/'
print(f'Loading courses from {url}')
r = requests.get(url)
response = r.json()

# Asumiendo que la respuesta es una lista de cursos
available_courses = [course['title'] for course in response]

print(f'Available courses: {", ".join(available_courses)}')

for course in response:
    course_id = course['id']
    course_title = course['title']
    r = requests.post(
        f'{base_url}courses/{course_id}/enroll/',
        auth=(username, password)
    )
    if r.status_code == 200:
        print(f'Successfully enrolled in {course_title}')
