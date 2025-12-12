from django.urls import path
from .views import ListaCreateView, ListaDeleteView, ListaUpdateView  # ¡Cambia a las CLASES!

app_name = 'lista'

urlpatterns = [
    path('crear/<int:tablero_pk>/', ListaCreateView.as_view(), name='create'),  # .as_view() para clases
    path('<int:pk>/eliminar/', ListaDeleteView.as_view(), name='delete'), 
    path('<int:pk>/editar/', ListaUpdateView.as_view(), name='update'), # .as_view() para clases
]