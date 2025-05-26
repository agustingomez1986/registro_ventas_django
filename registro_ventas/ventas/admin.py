from django.contrib import admin
from .models import Venta, Producto, VentaItem

admin.site.register([Venta, Producto, VentaItem])

