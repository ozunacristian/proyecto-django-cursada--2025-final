from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from apps.lista.models import Lista
from apps.ticket.models import Ticket
from apps.usuario.permissions import tableros_visibles_para_usuario

User = get_user_model()


def _usuarios_asignables_para_tablero(tablero):
    return User.objects.filter(
        Q(tableros_creados=tablero) | Q(tableros_como_miembro__tablero=tablero)
    ).distinct()


class TicketCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Ticket
    template_name = 'ticket/ticket_form.html'
    fields = ['titulo', 'descripcion', 'prioridad']
    permission_required = 'ticket.add_ticket'

    def _get_lista(self):
        return get_object_or_404(
            Lista.objects.filter(tablero__in=tableros_visibles_para_usuario(self.request.user)),
            pk=self.kwargs['lista_pk'],
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lista'] = self._get_lista()
        return context

    def form_valid(self, form):
        lista = self._get_lista()
        form.instance.lista = lista
        form.instance.tablero = lista.tablero
        form.instance.creado_por = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('detalle_tablero', args=[self.object.tablero.pk])


class TicketDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Ticket
    template_name = 'ticket/detalle_ticket.html'
    context_object_name = 'ticket'
    permission_required = 'ticket.view_ticket'

    def get_queryset(self):
        return Ticket.objects.filter(
            tablero__in=tableros_visibles_para_usuario(self.request.user)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['etiquetas_disponibles'] = self.object.tablero.etiquetas.exclude(
            etiqueta_tickets__ticket=self.object
        )
        return context


class TicketUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Ticket
    template_name = 'ticket/ticket_form.html'
    fields = ['titulo', 'descripcion', 'lista', 'prioridad']
    permission_required = 'ticket.change_ticket'

    def get_queryset(self):
        return Ticket.objects.filter(
            tablero__in=tableros_visibles_para_usuario(self.request.user)
        )

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['lista'].queryset = Lista.objects.filter(tablero=self.object.tablero)
        return form

    def form_valid(self, form):
        if 'lista' in form.changed_data:
            messages.info(self.request, f'Ticket movido a "{form.cleaned_data["lista"].titulo}"')
        messages.success(self.request, f'Ticket "{form.instance.titulo}" actualizado!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('detalle_tablero', args=[self.object.tablero.pk])


class TicketMoveView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'ticket.change_ticket'

    def post(self, request, pk):
        ticket = get_object_or_404(
            Ticket.objects.filter(tablero__in=tableros_visibles_para_usuario(request.user)),
            pk=pk,
        )
        lista_destino_id = request.POST.get('lista_destino_id')
        if not lista_destino_id:
            messages.error(request, 'Debes seleccionar una lista de destino.')
            return redirect('detalle_tablero', pk=ticket.tablero.pk)

        lista_destino = get_object_or_404(
            Lista.objects.filter(tablero=ticket.tablero),
            pk=lista_destino_id,
        )
        if ticket.lista_id == lista_destino.pk:
            messages.info(request, f'El ticket ya está en "{lista_destino.titulo}".')
            return redirect('detalle_tablero', pk=ticket.tablero.pk)

        ticket.lista = lista_destino
        ticket.save()
        messages.success(request, f'Ticket movido a "{lista_destino.titulo}".')
        return redirect('detalle_tablero', pk=ticket.tablero.pk)


class TicketDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Ticket
    template_name = 'ticket/eliminar_ticket.html'
    permission_required = 'ticket.delete_ticket'

    def get_queryset(self):
        return Ticket.objects.filter(
            tablero__in=tableros_visibles_para_usuario(self.request.user)
        )

    def delete(self, request, *args, **kwargs):
        ticket = self.get_object()
        messages.success(request, f'Ticket "{ticket.titulo}" eliminado!')
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('detalle_tablero', args=[self.object.tablero.pk])
