from django.db.models import Q

from apps.tablero.models import Tablero


def tableros_visibles_para_usuario(user):
    if user.is_superuser:
        return Tablero.objects.all()

    return Tablero.objects.filter(
        Q(creado_por=user) | Q(integrantes__usuario=user)
    ).distinct()
