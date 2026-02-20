from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from apps.tablero.models import Tablero
from apps.usuario.permissions import tableros_visibles_para_usuario


class TableroListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Tablero
    template_name = 'tablero/lista.html'
    permission_required = 'tablero.view_tablero'

    def get_queryset(self):
        return tableros_visibles_para_usuario(self.request.user)


class TableroDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Tablero
    template_name = 'tablero/detalle.html'
    permission_required = 'tablero.view_tablero'

    def get_queryset(self):
        return tableros_visibles_para_usuario(self.request.user)


class TableroCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Tablero
    template_name = 'tablero/formulario.html'
    fields = ['titulo', 'descripcion']
    success_url = reverse_lazy('lista_tableros')
    permission_required = 'tablero.add_tablero'

    def form_valid(self, form):
        form.instance.creado_por = self.request.user
        return super().form_valid(form)


class TableroUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Tablero
    template_name = 'tablero/formulario.html'
    fields = ['titulo', 'descripcion']
    success_url = reverse_lazy('lista_tableros')
    permission_required = 'tablero.change_tablero'

    def get_queryset(self):
        return tableros_visibles_para_usuario(self.request.user)


class TableroDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Tablero
    template_name = 'tablero/eliminar.html'
    success_url = reverse_lazy('lista_tableros')
    permission_required = 'tablero.delete_tablero'

    def get_queryset(self):
        return tableros_visibles_para_usuario(self.request.user)
