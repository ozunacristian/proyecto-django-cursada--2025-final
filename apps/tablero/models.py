from django.db import models
from django.contrib.auth.models import User


class Tablero(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tableros_creados')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

class IntegranteTablero(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tableros_como_miembro')
    tablero = models.ForeignKey(Tablero, on_delete=models.CASCADE, related_name='integrantes')
    fecha_union = models.DateTimeField(auto_now_add=True)

    class Meta: 
        unique_together = ('usuario', 'tablero')
        verbose_name = 'Integrante del Tablero'
        verbose_name_plural = 'Integrantes del Tablero'

    def __str__(self):
        return f"{self.usuario.username} → {self.tablero.titulo}"