from django.urls import path

from apps.usuario.views import PerfilUsuarioView, UsuarioLoginView, UsuarioLogoutView

app_name = 'usuario'

urlpatterns = [
    path('', UsuarioLoginView.as_view(), name='login'), # raiz de la app y del sitio.
    path('logout/', UsuarioLogoutView.as_view(), name='logout'),
    path('perfil/', PerfilUsuarioView.as_view(), name='perfil'),
]
