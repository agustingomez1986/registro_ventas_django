from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuarios(AbstractUser):
    telefono = models.CharField(max_length=14)
    interno = models.BooleanField(default=False, verbose_name='¿Pertenece a la cooperativa?')

class Retiros(models.Model):
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name='retiros')
    monto = models.DecimalField(max_digits=10, decimal_places=2)