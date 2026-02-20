from django.conf import settings
from django.db import models


class PerfilUsuario(models.Model):
    class Rol(models.TextChoices):
        ADMIN = 'admin', 'Administrador'
        SUPERVISOR = 'supervisor', 'Supervisor'
        EMPLEADO = 'empleado', 'Empleado'
        CLIENTE = 'cliente', 'Cliente'

    ROLE_GROUP_MAP = {
        Rol.ADMIN: 'Rol Administrador',
        Rol.SUPERVISOR: 'Rol Supervisor',
        Rol.EMPLEADO: 'Rol Empleado',
        Rol.CLIENTE: 'Rol Cliente',
    }

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='perfil')
    rol = models.CharField(max_length=20, choices=Rol.choices, default=Rol.EMPLEADO)

    def __str__(self):
        return f"{self.user.username} ({self.get_rol_display()})"
