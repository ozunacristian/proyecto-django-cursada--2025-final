from django.db import models
from django.contrib.auth.models import User


class Lista(models.Model):
    titulo = models.CharField(max_length=200)
    orden = models.PositiveIntegerField(default=1) # restrigimos a valores positivos iniciando en 1.
    tablero = models.ForeignKey('tablero.Tablero', on_delete=models.CASCADE, related_name='listas') # cada "columna" pertenece a un tablero.
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['orden'] # esto es para ordenar las "columnas"
        verbose_name = 'Lista'
        verbose_name_plural = 'Listas'
        unique_together = ('tablero', 'orden') # para que no se pueda poner una lista en el mismo lugar de otra. (el id de tablero junto al valor de orden son únicos)

    def __str__(self):
        return f"{self.titulo} ({self.tablero.titulo})"

class Ticket(models.Model):

    # De momento se harcodea la prioridad, se prevee expansión con un modelo como lookUp, dado que pueden haber más categorías de prioridad.
    PRIORIDAD_CHOICES = [
        (1, 'Baja'),
        (2, 'Media'),
        (3, 'Alta'),
    ]

    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    tablero = models.ForeignKey('tablero.Tablero', on_delete=models.CASCADE, related_name='tickets')
    lista = models.ForeignKey(Lista, on_delete=models.CASCADE, related_name='tickets')

    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='tickets_creados') # consideramos ideal nulleable por si el usuario relacionado cambia o es borrado.
    asignado_a = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets_asignados')

    prioridad = models.IntegerField(choices=PRIORIDAD_CHOICES, default=2)

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['-fecha_creacion'] # ordenamos por fecha.
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'

    def __str__(self):
        return f"{self.titulo} ({self.lista.titulo})"




