from django.urls import path
from . import views

urlpatterns = [
    path('registro', views.registrar_venta, name='venta'),
    path('ventas', views.VentaListView.as_view(), name='listado_ventas'),
]