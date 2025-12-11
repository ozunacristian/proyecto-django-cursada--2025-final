from django.db import models
from django.contrib.auth.models import User


class PerfilUsuario(models.Model):
    # Opciones para el rol
    OPCIONES_ROLES = [
        ('admin', 'Administrador'),
        ('supervisor', 'Supervisor'),
        ('empleado', 'Empleado'),
        ('cliente', 'Cliente'),
    ]

    # Relación 1:1 con User
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    
    # Seleccion de rol
    rol = models.CharField(max_length=20, choices=OPCIONES_ROLES)

    def __str__(self):
        return f"{self.user.username} ({self.get_rol_display()})"
