from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from apps.ticket.models import Ticket
from apps.usuario.permissions import tableros_visibles_para_usuario
from .models import Comentario


class ComentarioCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Comentario
    template_name = 'comentario/comentario_form.html'
    fields = ['contenido']
    permission_required = 'comentario.add_comentario'

    def _get_ticket(self):
        return get_object_or_404(
            Ticket.objects.filter(tablero__in=tableros_visibles_para_usuario(self.request.user)),
            pk=self.kwargs['ticket_pk'],
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ticket'] = self._get_ticket()
        return context

    def form_valid(self, form):
        form.instance.ticket = self._get_ticket()
        form.instance.usuario = self.request.user
        messages.success(self.request, 'Comentario agregado correctamente.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('ticket:detalle_ticket', args=[self.object.ticket.pk])


class ComentarioUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Comentario
    template_name = 'comentario/comentario_form.html'
    fields = ['contenido']
    context_object_name = 'comentario'
    permission_required = 'comentario.change_comentario'

    def get_queryset(self):
        return Comentario.objects.filter(
            ticket__tablero__in=tableros_visibles_para_usuario(self.request.user)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ticket'] = self.object.ticket
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Comentario actualizado correctamente.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('ticket:detalle_ticket', args=[self.object.ticket.pk])


class ComentarioDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Comentario
    template_name = 'comentario/eliminar_comentario.html'
    context_object_name = 'comentario'
    permission_required = 'comentario.delete_comentario'

    def get_queryset(self):
        return Comentario.objects.filter(
            ticket__tablero__in=tableros_visibles_para_usuario(self.request.user)
        )

    def delete(self, request, *args, **kwargs):
        comentario = self.get_object()
        messages.success(request, 'Comentario eliminado correctamente.')
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('ticket:detalle_ticket', args=[self.object.ticket.pk])
