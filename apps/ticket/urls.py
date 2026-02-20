from django.urls import path
from .views import TicketCreateView, TicketDetailView, TicketUpdateView, TicketDeleteView

app_name = 'ticket'

urlpatterns = [
    path('crear/<int:lista_pk>/', TicketCreateView.as_view(), name='crear_ticket'),
    path('<int:pk>/', TicketDetailView.as_view(), name='detalle_ticket'),
    path('<int:pk>/editar/', TicketUpdateView.as_view(), name='editar_ticket'),
    path('<int:pk>/eliminar/', TicketDeleteView.as_view(), name='eliminar_ticket'),
]