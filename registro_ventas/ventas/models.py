from django.db import models

CUENTA_TRANSFERENCIA_CHOICES = [
    ('Vale', 'Vale'),
    ('Dani', 'Dani'),
    ('Vero', 'Vero'),
]


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    codigo_hacedor = models.CharField(max_length=4)

class Venta(models.Model):
    METODO_PAGO_CHOICES = [
        ('EF', 'Efectivo'),
        ('TR', 'Transferencia'),
    ]

    usuario = models.ForeignKey('usuarios.Usuarios', on_delete=models.CASCADE, related_name='ventas')
    fecha = models.DateTimeField(auto_now_add=True)
    metodo_pago = models.CharField(max_length=2, choices=METODO_PAGO_CHOICES)
    cuenta_transferencia = models.CharField(max_length=20, choices=CUENTA_TRANSFERENCIA_CHOICES, blank=True, null=True)
    total = models.DecimalField(max_digits=8, decimal_places=2)

class VentaItem(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=8, decimal_places=2)
    