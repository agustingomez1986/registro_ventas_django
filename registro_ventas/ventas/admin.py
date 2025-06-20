from django.contrib import admin
from .models import Venta, VentaItem

admin.site.register([Venta, VentaItem])

