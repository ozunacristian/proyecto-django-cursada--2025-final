from django.contrib import admin
from apps.tablero.models import Tablero, IntegranteTablero


@admin.register(Tablero)
class TableroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'creado_por', 'fecha_creacion')
    list_filter = ('creado_por', 'fecha_creacion')
    search_fields = ('titulo', 'descripcion')
    ordering = ('-fecha_creacion',)

@admin.register(IntegranteTablero)
class IntegranteTableroAdmin(admin.ModelAdmin):
    list_display = ('usuario_username', 'tablero', 'fecha_union')
    list_filter = ('tablero', 'fecha_union')
    search_fields = ('usuario__username', 'tablero__titulo')

    def usuario_username(self, obj):
        return obj.usuario.username

    usuario_username.short_description = 'Usuario'