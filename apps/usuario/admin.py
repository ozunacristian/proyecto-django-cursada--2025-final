from django.contrib import admin
from apps.usuario.models import PerfilUsuario

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario_username', 'rol')

    # Esto permite mostrar el username del User relacionado
    def usuario_username(self, obj):
        return obj.user.username
    
    usuario_username.short_description = 'Usuario'
