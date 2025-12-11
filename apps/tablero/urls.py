from django.urls import path
from apps.tablero.views import TableroListView, TableroDetailView, TableroCreateView, TableroDeleteView

urlpatterns = [
    path('', TableroListView.as_view(), name='lista_tableros'),
    path('<int:pk>/', TableroDetailView.as_view(), name='detalle_tablero'),
    path('crear/', TableroCreateView.as_view(), name='crear_tablero'),
    path('<int:pk>/eliminar/', TableroDeleteView.as_view(), name='eliminar_tablero'),
]