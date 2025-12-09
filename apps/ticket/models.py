from django.db import models
from apps.tablero.models import Tablero


class Lista(models.Model):
    titulo = models.CharField(max_length=200)
    orden = models.PositiveIntegerField(default=1)
    tablero = models.ForeignKey(Tablero, on_delete=models.CASCADE, related_name='listas') # cada "columna" pertenece a un tablero.
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['orden'] # esto es para ordenar las "columnas"
        verbose_name = 'Lista'
        verbose_name_plural = 'Listas'
        unique_together = ('tablero', 'orden') # para que no se pueda poner una lista en el mismo lugar de otra.

    def __str__(self):
        return f"{self.titulo} ({self.tablero.titulo})"
