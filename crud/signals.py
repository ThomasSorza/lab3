from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps

from .models import Users, Roles_Users

@receiver(post_save, sender=Users)
def create_roles_users(sender, instance, created, **kwargs):
    """
    Esta función se ejecutará después de guardar un usuario.
    Crea un nuevo registro en Roles_Users con el ID del usuario y el ID del rol.
    """
    if created:
        # 'instance' es la instancia recién creada del modelo Users
        # Puedes personalizar cómo obtienes el rol asociado según tu lógica
        role_instance = instance.role

        # Crea una nueva instancia de Roles_Users y asigna el usuario y el rol
        roles_users_instance = Roles_Users(user=instance, role=role_instance)

        # Guarda la instancia en la base de datos
        roles_users_instance.save()

# Registra las señales al cargar la aplicación
post_save.connect(create_roles_users, sender=Users)
