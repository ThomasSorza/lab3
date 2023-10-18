#Manual pagination
#2nd pagination option (1st option in settings.py)
#http://127.0.0.1:8000/users/?page=(num pag here)
#Sample: http://127.0.0.1:8000/users/?page=3
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination

class CreatePageNumberPagination(PageNumberPagination):
    #Read all about 
    #https://www.django-rest-framework.org/api-guide/pagination/
    #contains params, etc
    page_size = 50 #results's size (show first 50 registers)