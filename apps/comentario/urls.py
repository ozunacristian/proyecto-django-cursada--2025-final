from django.urls import path

from .views import ComentarioCreateView, ComentarioDeleteView, ComentarioUpdateView

app_name = 'comentario'

urlpatterns = [
    path('crear/<int:ticket_pk>/', ComentarioCreateView.as_view(), name='crear'),
    path('<int:pk>/editar/', ComentarioUpdateView.as_view(), name='editar'),
    path('<int:pk>/eliminar/', ComentarioDeleteView.as_view(), name='eliminar'),
]
