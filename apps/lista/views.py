from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin  #protec que aún no utilizamos pero lo dejams para más adelante
from django.urls import reverse_lazy
from django.contrib import messages  
from apps.tablero.models import Tablero
from .models import Lista

class ListaCreateView(CreateView):
    model = Lista
    template_name = 'lista/lista_form.html'
    fields = ['titulo']  
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tablero_id = self.kwargs['tablero_pk']
        context['tablero'] = Tablero.objects.get(pk=tablero_id)  
        return context
    
    def form_valid(self, form):
        tablero_id = self.kwargs['tablero_pk']
        tablero = Tablero.objects.get(pk=tablero_id)
        form.instance.tablero = tablero
        
        # genera un orden automatico, más adelante se podrá reordenar manualmente, por el momento dejamos como mvp este
        ultima_lista = Lista.objects.filter(tablero=tablero).order_by('-orden').first()
        if ultima_lista:
            form.instance.orden = ultima_lista.orden + 1
        else:
            form.instance.orden = 1
        
        messages.success(self.request, f'Lista "{form.instance.titulo}" creada exitosamente!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('detalle_tablero', args=[self.kwargs['tablero_pk']])

class ListaUpdateView(LoginRequiredMixin, UpdateView):  #LoginRequiredMixin agregado sin usar por el moment.
    model = Lista
    template_name = 'lista/lista_form.html'  #template unificado (unificamos create y update en uno solo.) 
    fields = ['titulo']
    context_object_name = 'lista'  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # agregar tablero al contexto para el template
        context['tablero'] = self.object.tablero
        return context

    def get_success_url(self):
        # mensaje de éxito de actualización
        messages.success(self.request, f'Lista "{self.object.titulo}" actualizada!')
        return reverse_lazy('detalle_tablero', args=[self.object.tablero.pk])

class ListaDeleteView(LoginRequiredMixin, DeleteView):  #LoginRequiredMixin agregado aún sin usar por el momento.

    model = Lista
    template_name = 'lista/eliminar_lista.html'  
    context_object_name = 'lista'  #nombre más claro

    def get_success_url(self):
        # mensaje de exito de eliminación
        messages.success(self.request, f'Lista "{self.object.titulo}" eliminada!')
        return reverse_lazy('detalle_tablero', args=[self.object.tablero.pk])