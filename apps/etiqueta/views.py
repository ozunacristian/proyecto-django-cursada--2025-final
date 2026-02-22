from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, UpdateView

from apps.ticket.models import Ticket
from apps.usuario.permissions import tableros_visibles_para_usuario
from .models import Etiqueta, EtiquetaTicket


class EtiquetaCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Etiqueta
    template_name = 'etiqueta/etiqueta_form.html'
    fields = ['nombre', 'color']
    permission_required = 'etiqueta.add_etiqueta'

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
        form.instance.tablero = self._get_tablero()
        messages.success(self.request, 'Etiqueta creada correctamente.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('detalle_tablero', args=[self.object.tablero.pk])


class EtiquetaUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Etiqueta
    template_name = 'etiqueta/etiqueta_form.html'
    fields = ['nombre', 'color']
    context_object_name = 'etiqueta'
    permission_required = 'etiqueta.change_etiqueta'

    def get_queryset(self):
        return Etiqueta.objects.filter(tablero__in=tableros_visibles_para_usuario(self.request.user))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tablero'] = self.object.tablero
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Etiqueta actualizada correctamente.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('detalle_tablero', args=[self.object.tablero.pk])


class EtiquetaDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Etiqueta
    template_name = 'etiqueta/eliminar_etiqueta.html'
    context_object_name = 'etiqueta'
    permission_required = 'etiqueta.delete_etiqueta'

    def get_queryset(self):
        return Etiqueta.objects.filter(tablero__in=tableros_visibles_para_usuario(self.request.user))

    def delete(self, request, *args, **kwargs):
        etiqueta = self.get_object()
        messages.success(request, f'Etiqueta "{etiqueta.nombre}" eliminada.')
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('detalle_tablero', args=[self.object.tablero.pk])


class EtiquetaAsignarTicketView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'etiqueta.change_etiqueta'

    def post(self, request, ticket_pk):
        ticket = get_object_or_404(
            Ticket.objects.filter(tablero__in=tableros_visibles_para_usuario(request.user)),
            pk=ticket_pk,
        )
        etiqueta_id = request.POST.get('etiqueta_id')
        if not etiqueta_id:
            messages.error(request, 'Debes seleccionar una etiqueta.')
            return redirect('ticket:detalle_ticket', pk=ticket.pk)

        etiqueta = get_object_or_404(Etiqueta, pk=etiqueta_id, tablero=ticket.tablero)

        try:
            EtiquetaTicket.objects.create(ticket=ticket, etiqueta=etiqueta)
            messages.success(request, f'Etiqueta "{etiqueta.nombre}" asignada al ticket.')
        except IntegrityError:
            messages.info(request, f'El ticket ya tiene la etiqueta "{etiqueta.nombre}".')

        return redirect('ticket:detalle_ticket', pk=ticket.pk)


class EtiquetaQuitarTicketView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'etiqueta.change_etiqueta'

    def post(self, request, relacion_pk):
        relacion = get_object_or_404(
            EtiquetaTicket.objects.filter(
                ticket__tablero__in=tableros_visibles_para_usuario(request.user)
            ),
            pk=relacion_pk,
        )
        ticket_pk = relacion.ticket.pk
        etiqueta_nombre = relacion.etiqueta.nombre
        relacion.delete()
        messages.success(request, f'Etiqueta "{etiqueta_nombre}" quitada del ticket.')
        return redirect('ticket:detalle_ticket', pk=ticket_pk)
