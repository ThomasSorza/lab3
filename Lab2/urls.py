
from django.contrib import admin
from django.urls import path, include
#imports for token authentication JWT
from crud.views import MyTokenObtainPairView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('crud.urls')),
]
