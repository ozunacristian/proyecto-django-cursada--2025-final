from django.db import models

class Etiqueta(models.Model):
    nombre = models.CharField(max_length=100)
    color = models.CharField(max_length=20, default="#cccccc")
    tablero = models.ForeignKey('tablero.Tablero', on_delete=models.CASCADE, related_name='etiquetas')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Etiqueta'
        verbose_name_plural = 'Etiquetas'
        ordering = ['nombre'] # Ordenamos alfabeticamente.

    def __str__(self):
        return f"{self.nombre} ({self.tablero.titulo})"

# con este modelo se podrá aplicar múltiples etiquetas a un ticket.
class EtiquetaTicket(models.Model):
    ticket = models.ForeignKey('ticket.Ticket', on_delete=models.CASCADE, related_name='ticket_etiquetas')
    etiqueta = models.ForeignKey('Etiqueta', on_delete=models.CASCADE, related_name='etiqueta_tickets')
    fecha_asignacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('ticket', 'etiqueta') # Asi evitamos que se pueda etiquetar más de una vez con la misma etiqueta a un ticket.
        verbose_name = 'Etiqueta aplicada al ticket'
        verbose_name_plural = 'Etiquetas aplicadas a tickets'

    def __str__(self):
        return f"{self.ticket.titulo} → {self.etiqueta.nombre}"
