from django.apps import AppConfig

class UsuariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usuarios'

    def ready(self):
        from django.contrib.auth.models import Group, Permission
        from django.contrib.contenttypes.models import ContentType
        from django.db.utils import OperationalError, ProgrammingError

        try:
            # Creo grupos
            grupo_administrador, _ = Group.objects.get_or_create(name='administrador')
            grupo_vendedor, _ = Group.objects.get_or_create(name='vendedor')

            # Obtengo los permisos del modelo
            content_type_usuarios = ContentType.objects.get(app_label='usuarios', model='usuarios')
            permiso_add_usuarios = Permission.objects.get(codename='add_usuarios', content_type=content_type_usuarios)

            # Asigno permisos
            grupo_administrador.permissions.add(permiso_add_usuarios)


        except (Permission.DoesNotExist, ContentType.DoesNotExist, OperationalError, ProgrammingError):
            pass