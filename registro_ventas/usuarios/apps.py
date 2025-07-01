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
            grupo_externo, _ = Group.objects.get_or_create(name='externo')

            # Obtengo los permisos del modelo
            content_type_usuarios = ContentType.objects.get(app_label='usuarios', model='usuarios')
            permiso_add_usuarios = Permission.objects.get(codename='add_usuarios', content_type=content_type_usuarios)
            permiso_change_usuarios = Permission.objects.get(codename='change_usuarios', content_type=content_type_usuarios)

            content_type_venta = ContentType.objects.get(app_label='ventas', model='venta')
            permiso_add_venta = Permission.objects.get(codename='add_venta', content_type=content_type_venta)
            permiso_view_venta = Permission.objects.get(codename='view_venta', content_type=content_type_venta)

            # Asigno permisos
            grupo_administrador.permissions.add(permiso_add_usuarios)
            grupo_administrador.permissions.add(permiso_add_venta)
            grupo_administrador.permissions.add(permiso_view_venta)
            grupo_administrador.permissions.add(permiso_change_usuarios)
            grupo_vendedor.permissions.add(permiso_add_venta)
            grupo_vendedor.permissions.add(permiso_view_venta)
            grupo_externo.permissions.add(permiso_view_venta)

        except (Permission.DoesNotExist, ContentType.DoesNotExist, OperationalError, ProgrammingError):
            pass