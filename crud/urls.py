from django.urls import path
from . import views

urlpatterns = [
    #users paths
    path('', views.getRoutes),
    #path('token/', views.getRoutes),
    path('users/', views.UserListCreateView.as_view(), name='users-list-create'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='users-detail'),
    path('users/create-multiple/', views.CreateMultipleUsers.as_view(), name='create-multiple-users'),
    path('users-by-name/', views.UserByNameView.as_view(), name='user-by-name'), #Example http://localhost:2000/users-by-name/?name=Esteban
    path('users/<int:pk>/delete-id/', views.DeleteUserById.as_view(), name='delete-by-id'), #Example http://localhost:2000/users/<int:pk>/delete-id/
    #path('users/<str:name>', views.UserRoles.as_view(), name='user-roles'
    #roles paths
    path('roles/', views.RoleListCreateView.as_view(), name='roles-list-create'),
    path('roles/create-multiple/', views.CreateMultipleRoles.as_view(), name='create-multiple-roles'),
    path('roles/<int:pk>/', views.RoleDetailView.as_view(), name='roles-detail'),
]