from django.contrib import admin
from .models import Usuarios, Retiros

admin.site.register(Retiros)

@admin.register(Usuarios)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'email', 'telefono', 'interno']
    search_fields = ['first_name']
    list_filter = ['interno']