from django.urls import path

from apps.usuario.views import PerfilUsuarioView, UsuarioLoginView, UsuarioLogoutView

app_name = 'usuario'

urlpatterns = [
    path('login/', UsuarioLoginView.as_view(), name='login'),
    path('logout/', UsuarioLogoutView.as_view(), name='logout'),
    path('perfil/', PerfilUsuarioView.as_view(), name='perfil'),
]
