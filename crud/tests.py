from django.shortcuts import render
from django.http import HttpResponse
from .models import Users, Roles
from .serializers import UsersSerializer, RolesSerializer
from rest_framework import generics


# Create your views here.
# TODO: add a view (Actually not allowed for lab #2)
def index(request):
    return HttpResponse("<h1> Lab #2: A simple CRUD with HTTP. <br> Hello World!</h1>")

class UserListCreateView(generics.ListCreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

class RoleListCreateView(generics.ListCreateAPIView):
    queryset = Roles.objects.all()
    serializer_class = RolesSerializer

class RoleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Roles.objects.all()
    serializer_class = RolesSerializer