from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from apps.ticket.models import Ticket
from apps.lista.models import Lista
from django.urls import reverse_lazy
from django.contrib import messages

class TicketCreateView(CreateView):
    model = Ticket
    template_name = 'ticket/ticket_form.html'
    fields = ['titulo', 'descripcion', 'prioridad', 'asignado_a']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lista = Lista.objects.get(pk=self.kwargs['lista_pk'])
        context['lista'] = lista
        return context

    def form_valid(self, form):
        lista = Lista.objects.get(pk=self.kwargs['lista_pk'])
        form.instance.lista = lista
        form.instance.tablero = lista.tablero
        form.instance.creado_por = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('detalle_tablero', args=[self.object.tablero.pk])

class TicketDetailView(DetailView):
    model = Ticket
    template_name = 'ticket/detalle_ticket.html'
    context_object_name = 'ticket'

class TicketUpdateView(UpdateView):
    model = Ticket
    template_name = 'ticket/ticket_form.html'
    fields = ['titulo', 'descripcion', 'lista', 'prioridad', 'asignado_a']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['lista'].queryset = Lista.objects.filter(
            tablero=self.object.tablero
        )
        return form

    def form_valid(self, form):
        # Detectar si se cambió la lista
        if 'lista' in form.changed_data:
            messages.info(self.request, f'Ticket movido a "{form.cleaned_data["lista"].titulo}"')
        messages.success(self.request, f'Ticket "{form.instance.titulo}" actualizado!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('detalle_tablero', args=[self.object.tablero.pk])

class TicketDeleteView(DeleteView):
    model = Ticket
    template_name = 'ticket/eliminar_ticket.html'

    def delete(self, request, *args, **kwargs):
        ticket = self.get_object()
        messages.success(request, f'Ticket "{ticket.titulo}" eliminado!')
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('detalle_tablero', args=[self.object.tablero.pk])