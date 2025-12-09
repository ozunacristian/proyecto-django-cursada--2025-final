from django.contrib import admin
from apps.ticket.models import Lista, Ticket, Tag


@admin.register(Lista)
class ListaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tablero', 'orden', 'fecha_creacion')
    list_filter = ('tablero',)
    search_fields = ('titulo', 'tablero__titulo')
    ordering = ('tablero', 'orden')

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tablero', 'lista', 'creado_por', 'asignado_a', 'prioridad', 'fecha_creacion')
    list_filter = ('tablero', 'lista', 'prioridad', 'activo')
    search_fields = ('titulo', 'descripcion', 'creado_por__username', 'asignado_a__username')
    ordering = ('-fecha_creacion',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'color', 'tablero', 'fecha_creacion')
    list_filter = ('tablero',)
    search_fields = ('nombre', 'tablero__titulo')
    ordering = ('tablero', 'nombre')
