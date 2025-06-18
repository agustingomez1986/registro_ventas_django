from django.urls import path
from django.http import HttpResponse
from . import views

urlpatterns = [
    path('', views.login_usuario, name='login'),  # /usuarios/
    path('perfil', views.perfil, name='perfil'),    # /usuarios/perfil/
    path('registro', views.registrar_usuario, name='registro'),
    path('registro_exitoso', lambda r: HttpResponse('Registro exitoso'), name='registro_exitoso'),
]