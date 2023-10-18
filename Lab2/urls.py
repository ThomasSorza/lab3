from django.contrib import admin
from django.urls import path, include
#imports for token authentication JWT
from crud.views import MyTokenObtainPairView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    #paths for token authentication JWT
    path('admin/', admin.site.urls),
    path('crud/', include('crud.urls')),
    #path('', include('crud.urls')),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
