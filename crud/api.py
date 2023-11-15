from rest_framework import viewsets, permissions
from .serializers import UsersSerializer, RolesSerializer
from rest_framework import status
from rest_framework.response import Response
from .models import Roles, Users
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter, OrderingFilter

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 50

class UsersSearch(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    pagination_class = CustomPageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('first_name', 'last_name')
    ordering_fields = ('first_name', 'last_name')  # Add the fields you want to support ordering

class RolesViewSet(viewsets.ModelViewSet):
    queryset = Roles.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RolesSerializer
    pagination_class = CustomPageNumberPagination

    def delete_all_roles(self, request):
        Roles.objects.all().delete()
        return Response({"message": "Todos los roles han sido eliminados"}, status=status.HTTP_204_NO_CONTENT)

class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UsersSerializer
    pagination_class = CustomPageNumberPagination

    def delete_all_users(self, request):
        Users.objects.all().delete()
        return Response({"message": "Todos los usuarios han sido eliminados"}, status=status.HTTP_204_NO_CONTENT)

class RolesViewSetM(viewsets.ModelViewSet):
    queryset = Roles.objects.all()
    serializer_class = RolesSerializer

    def create(self, request, *args, **kwargs):
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
