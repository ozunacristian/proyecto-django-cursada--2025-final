from django.db import models

class Lista(models.Model):
    titulo = models.CharField(max_length=200)
    orden = models.PositiveIntegerField(default=1) # restrigimos a valores positivos iniciando en 1.
    tablero = models.ForeignKey('tablero.Tablero', on_delete=models.CASCADE, related_name='listas') # cada "columna" pertenece a un tablero.
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['orden'] # esto es para ordenar las "columnas"
        verbose_name = 'Lista'
        verbose_name_plural = 'Listas'
        unique_together = ('tablero', 'orden') # para que no se pueda posicionar una lista en el mismo lugar de otra. (el id de tablero junto al valor de orden son únicos)

    def __str__(self):
        return f"{self.titulo} ({self.tablero.titulo})"
