from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.login_usuario, name='login'),  # /usuarios/
    path('perfil', views.perfil, name='perfil'),    # /usuarios/perfil/
    path('registro', views.registrar_usuario, name='signup'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
]