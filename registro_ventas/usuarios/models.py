from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuarios(AbstractUser):
    telefono = models.CharField(max_length=14)
    interno = models.BooleanField(default=False, verbose_name='¿Pertenece a la cooperativa?')
    cuenta_transferencia = models.CharField(blank=True, null=True)

class Retiros(models.Model):
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name='retiros')
    monto = models.DecimalField(max_digits=10, decimal_places=2)

class Emprendimiento(models.Model):
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name='emprendimiento')
    nombre_emprendimiento = models.CharField(max_length=50, unique=True, blank=False, null=False)
    codigo_emprendimiento = models.CharField(max_length=4, unique=True, blank=False, null=False)

    def __str__(self):
        return f'{self.nombre_emprendimiento} ({self.codigo_emprendimiento})'