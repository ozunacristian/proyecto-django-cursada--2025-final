from django.contrib import admin
from apps.tablero.models import Tablero


@admin.register(Tablero)
class TableroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'creado_por', 'fecha_creacion')
    list_filter = ('creado_por', 'fecha_creacion')
    search_fields = ('titulo', 'descripcion')
    ordering = ('-fecha_creacion',)
