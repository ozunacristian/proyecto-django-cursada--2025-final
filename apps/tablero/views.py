from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.urls import reverse_lazy
from apps.tablero.models import Tablero

class TableroListView(ListView):
    model = Tablero
    template_name = 'tablero/lista_tableros.html'
    context_object_name = 'tableros'

class TableroDetailView(DetailView):
    model = Tablero
    template_name = 'tablero/detalle_tablero.html'
    context_object_name = 'tablero'

class TableroCreateView(CreateView):
    model = Tablero
    template_name = 'tablero/crear_tablero.html'
    fields = ['titulo', 'descripcion', 'creado_por']
    success_url = reverse_lazy('lista_tableros')

class TableroDeleteView(DeleteView):
    model = Tablero
    template_name = 'tablero/confirmar_eliminar_tablero.html'
    success_url = reverse_lazy('lista_tableros')

