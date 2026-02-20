from django.db import models
from django.contrib.auth.models import User

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
    lista = models.ForeignKey('lista.Lista', on_delete=models.CASCADE, related_name='tickets')

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




