from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = (self.request.GET.get('q') or '').strip()

        # El buscador se resuelve en backend para tener consistencia con paginación,
        # permisos y futuros filtros adicionales (prioridad/asignado).
        tickets_qs = self.object.tickets.select_related('asignado_a')
        if query:
            tickets_qs = tickets_qs.filter(
                Q(titulo__icontains=query) | Q(descripcion__icontains=query)
            )

        tickets_por_lista = {}
        for ticket in tickets_qs:
            tickets_por_lista.setdefault(ticket.lista_id, []).append(ticket)

        # Inyectamos una colección por lista para que el template no haga "lógica compleja"
        # con diccionarios dinámicos.
        listas = list(self.object.listas.all())
        for lista in listas:
            lista.tickets_filtrados = tickets_por_lista.get(lista.id, [])

        context['listas'] = listas
        context['q'] = query
        context['total_tickets_filtrados'] = tickets_qs.count()
        return context


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
