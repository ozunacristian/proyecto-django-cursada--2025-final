from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from apps.usuario.permissions import tableros_visibles_para_usuario
from .models import Lista


class ListaCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Lista
    template_name = 'lista/lista_form.html'
    fields = ['titulo']
    permission_required = 'lista.add_lista'

    def _get_tablero(self):
        return get_object_or_404(
            tableros_visibles_para_usuario(self.request.user),
            pk=self.kwargs['tablero_pk'],
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tablero'] = self._get_tablero()
        return context

    def form_valid(self, form):
        tablero = self._get_tablero()
        form.instance.tablero = tablero

        ultima_lista = Lista.objects.filter(tablero=tablero).order_by('-orden').first()
        if ultima_lista:
            form.instance.orden = ultima_lista.orden + 1
        else:
            form.instance.orden = 1

        messages.success(self.request, f'Lista "{form.instance.titulo}" creada exitosamente!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('detalle_tablero', args=[self.kwargs['tablero_pk']])


class ListaUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Lista
    template_name = 'lista/lista_form.html'
    fields = ['titulo']
    context_object_name = 'lista'
    permission_required = 'lista.change_lista'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tablero'] = self.object.tablero
        return context

    def get_queryset(self):
        return Lista.objects.filter(
            tablero__in=tableros_visibles_para_usuario(self.request.user)
        )

    def get_success_url(self):
        messages.success(self.request, f'Lista "{self.object.titulo}" actualizada!')
        return reverse_lazy('detalle_tablero', args=[self.object.tablero.pk])


class ListaDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Lista
    template_name = 'lista/eliminar_lista.html'
    context_object_name = 'lista'
    permission_required = 'lista.delete_lista'

    def get_queryset(self):
        return Lista.objects.filter(
            tablero__in=tableros_visibles_para_usuario(self.request.user)
        )

    def get_success_url(self):
        messages.success(self.request, f'Lista "{self.object.titulo}" eliminada!')
        return reverse_lazy('detalle_tablero', args=[self.object.tablero.pk])
