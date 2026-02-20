from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView


class UsuarioLoginView(LoginView):
    template_name = 'usuario/login.html'
    redirect_authenticated_user = True


class UsuarioLogoutView(LogoutView):
    next_page = 'usuario:login'


class PerfilUsuarioView(LoginRequiredMixin, TemplateView):
    template_name = 'usuario/perfil.html'
    login_url = 'usuario:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['perfil'] = getattr(self.request.user, 'perfil', None)
        return context
