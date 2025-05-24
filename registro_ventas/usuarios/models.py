from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuarios(AbstractUser):
    telefono = models.CharField(max_length=14)
