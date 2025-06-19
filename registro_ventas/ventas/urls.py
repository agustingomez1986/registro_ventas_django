from django.urls import path
from . import views

urlpatterns = [
    path('', views.ventas, name='ventas'),
    path('registro', views.registrar_venta, name='venta')
]