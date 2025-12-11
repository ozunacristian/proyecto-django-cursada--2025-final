from django.contrib import admin
from apps.etiqueta.models import Etiqueta, EtiquetaTicket

@admin.register(Etiqueta)
class EtiquetaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'color', 'tablero', 'fecha_creacion')
    list_filter = ('tablero',)
    search_fields = ('nombre', 'tablero__titulo')
    ordering = ('tablero', 'nombre')

@admin.register(EtiquetaTicket)
class EtiquetaTicketAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'etiqueta', 'fecha_asignacion')
    list_filter = ('etiqueta', 'ticket')
    search_fields = ('ticket__titulo', 'etiqueta__nombre')
    ordering = ('-fecha_asignacion',)
