from django.db import models
from django.utils.timezone import now

class Venta(models.Model):
    METODO_PAGO_CHOICES = [
        ('EF', 'Efectivo'),
        ('TR', 'Transferencia'),
    ]

    TURNO_CHOICES = [
        ('M', 'Mañana'),
        ('T', 'Tarde'),
    ]

    usuario = models.ForeignKey('usuarios.Usuarios', on_delete=models.CASCADE, related_name='ventas')
    fecha = models.DateTimeField(default=now)
    turno = models.CharField(max_length=1, choices=TURNO_CHOICES, default='M')
    metodo_pago = models.CharField(max_length=2, choices=METODO_PAGO_CHOICES)
    cuenta_transferencia = models.CharField(default=None, blank=True, null=True)
    total_a_cobrar = models.DecimalField(max_digits=8, decimal_places=2)
    total_cobrado = models.DecimalField(max_digits=8, decimal_places=2)

class VentaItem(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='items')
    producto = models.CharField(max_length=100)
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    codigo_emprendimiento = models.CharField(max_length=4, blank=False, null=False)
    codigo_producto = models.CharField(max_length=6, blank=True, null=True)
    