from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.tablero.models import Tablero
from django.contrib.auth.models import User

class TableroListView(ListView):
    model = Tablero
    template_name = 'tablero/lista.html'

class TableroDetailView(DetailView):
    model = Tablero
    template_name = 'tablero/detalle.html'

class TableroCreateView(CreateView):
    model = Tablero
    template_name = 'tablero/formulario.html'
    fields = ['titulo', 'descripcion']  # IMPORTANTE: solo estos campos
    success_url = reverse_lazy('lista_tableros')
    
    def form_valid(self, form):
        # Para pruebas, asigna el primer usuario que encuentre
        user = User.objects.first()
        form.instance.creado_por = user
        return super().form_valid(form)

class TableroUpdateView(UpdateView):
    model = Tablero
    template_name = 'tablero/formulario.html'
    fields = ['titulo', 'descripcion']
    success_url = reverse_lazy('lista_tableros')

class TableroDeleteView(DeleteView):
    model = Tablero
    template_name = 'tablero/eliminar.html'
    success_url = reverse_lazy('lista_tableros')