from django.apps import AppConfig

class CrudConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crud'

    def ready(self):
        import crud.signals  # Importa las señales al cargar la aplicación
