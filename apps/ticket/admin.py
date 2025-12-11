from django.contrib import admin
from apps.ticket.models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tablero', 'lista', 'creado_por', 'asignado_a', 'prioridad', 'fecha_creacion')
    list_filter = ('tablero', 'lista', 'prioridad', 'activo')
    search_fields = ('titulo', 'descripcion', 'creado_por__username', 'asignado_a__username')
    ordering = ('-fecha_creacion',)