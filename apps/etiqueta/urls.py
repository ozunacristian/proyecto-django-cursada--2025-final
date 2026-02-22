from django.urls import path

from .views import (
    EtiquetaAsignarTicketView,
    EtiquetaCreateView,
    EtiquetaDeleteView,
    EtiquetaQuitarTicketView,
    EtiquetaUpdateView,
)

app_name = 'etiqueta'

urlpatterns = [
    path('crear/<int:tablero_pk>/', EtiquetaCreateView.as_view(), name='crear'),
    path('<int:pk>/editar/', EtiquetaUpdateView.as_view(), name='editar'),
    path('<int:pk>/eliminar/', EtiquetaDeleteView.as_view(), name='eliminar'),
    path('ticket/<int:ticket_pk>/asignar/', EtiquetaAsignarTicketView.as_view(), name='asignar_ticket'),
    path('ticket/relacion/<int:relacion_pk>/quitar/', EtiquetaQuitarTicketView.as_view(), name='quitar_ticket'),
]
