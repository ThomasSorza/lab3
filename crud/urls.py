from rest_framework import routers
from .api import RolesViewSet, UsersViewSet, RolesViewSetM, UsersViewSetM, upload_image
from django.urls import path, include, re_path
from . import views

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = routers.DefaultRouter()
router.register('api/roles', RolesViewSet, 'roles')
router.register('api/users', UsersViewSet, 'users')
router.register('api/roles-m', RolesViewSetM, 'roles')
router.register('api/users-m', UsersViewSetM, 'users')

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/roles/delete-all/', RolesViewSet.as_view({'delete': 'delete_all_roles'}), name='delete-all-roles'),
    path('api/users/delete-all/', UsersViewSet.as_view({'delete': 'delete_all_users'}), name='delete-all-users'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('post_image/', upload_image, name='post-user-image'),
    re_path('login', views.login, name='login'),
    re_path('test_token', views.test_token, name='test_token'),
    #re_path('sign_up', views.sign_up, name='test_token'),
    path('', include(router.urls)),
    ]