from rest_framework.pagination import PageNumberPagination


# Heredamos de PageNumberPagination --> Proporciona soporte para la paginacion basada en nùmeros de pàgina.
class StandardPagination(PageNumberPagination):
    page_size = 10    # Determina el tamaño de pàginas predeterminado -- Nùmero de elementos devueltos por pàgina
    page_size_query_param = 'page_size'    # Definimos el nombre del paràmetro de consulta a utilizar para el tamaño de la pàgina
    max_page_size = 50    # Indica el tamaño màximo de pàginas solicitados permitido.

