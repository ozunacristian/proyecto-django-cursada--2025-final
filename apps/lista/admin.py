from django.contrib import admin
from apps.lista.models import Lista

@admin.register(Lista)
class ListaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tablero', 'orden', 'fecha_creacion')
    list_filter = ('tablero',)
    search_fields = ('titulo', 'tablero__titulo')
    ordering = ('tablero', 'orden')
