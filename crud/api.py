from rest_framework import viewsets, permissions
from .serializers import UsersSerializer, RolesSerializer

from rest_framework import status
from rest_framework.response import Response
import bcrypt
from .models import Roles, Users
from rest_framework.pagination import PageNumberPagination

class CustomPageNumberPagination(PageNumberPagination):
    #Read all about 
    #https://www.django-rest-framework.org/api-guide/pagination/
    #contains params, etc
    page_size = 50 #results's size (show first 50 registers)
    #max_page_size = 100

class RolesViewSet(viewsets.ModelViewSet):
    queryset = Roles.objects.all()
    permission_classes = [
        permissions.AllowAny  # TODO: Cambiar a IsAuthenticated
    ]
    serializer_class = RolesSerializer
    pagination_class = CustomPageNumberPagination

class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    permission_classes = [
        permissions.AllowAny  # TODO: Cambiar a IsAuthenticated
    ]
    serializer_class = UsersSerializer
    pagination_class = CustomPageNumberPagination

class RolesViewSetM(viewsets.ModelViewSet):
    queryset = Roles.objects.all()
    serializer_class = RolesSerializer

    def create(self, request, *args, **kwargs):
        # Handle bulk creation of roles
        roles_data = request.data if isinstance(request.data, list) else [request.data]
        roles_serializer = RolesSerializer(data=roles_data, many=True)

        if roles_serializer.is_valid():
            roles_serializer.save()
            return Response(roles_serializer.data, status=status.HTTP_201_CREATED)
        return Response(roles_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UsersViewSetM(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

    def create(self, request, *args, **kwargs):
        # Handle bulk creation of users
        users_data = request.data if isinstance(request.data, list) else [request.data]
        users_serializer = UsersSerializer(data=users_data, many=True)

        if users_serializer.is_valid():
            users_serializer.save()
            return Response(users_serializer.data, status=status.HTTP_201_CREATED)
        return Response(users_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from storages.backends.azure_storage import AzureStorage
from .forms import FileUploadForm

def upload_image(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            azure_storage = AzureStorage(
                account_name=settings.AZURE_ACCOUNT_NAME,
                account_key=settings.AZURE_ACCOUNT_KEY,
                container_name=settings.AZURE_CONTAINER,
            )
            azure_file_name = f'my_files/{file.name}'
            azure_storage.save(azure_file_name, file)
            return JsonResponse({'message': 'Archivo cargado con éxito en Azure Blob Storage.'})
        else:
            return JsonResponse({'error': 'Error en el formulario.'}, status=400)
    else:
        form = FileUploadForm()
    return render(request, 'upload_file.html', {'form': form})