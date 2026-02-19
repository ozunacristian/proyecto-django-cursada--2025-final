from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.usuario.models import PerfilUsuario

User = get_user_model()

MANAGED_APPS = {'tablero', 'lista', 'ticket', 'comentario', 'etiqueta', 'usuario'}

ROLE_PERMISSION_KEYS = {
    PerfilUsuario.Rol.ADMIN: 'admin',
    PerfilUsuario.Rol.SUPERVISOR: 'supervisor',
    PerfilUsuario.Rol.EMPLEADO: 'empleado',
    PerfilUsuario.Rol.CLIENTE: 'cliente',
}

ROLE_PERMISSIONS = {
    'supervisor': {
        ('tablero', 'add_tablero'),
        ('tablero', 'change_tablero'),
        ('tablero', 'delete_tablero'),
        ('tablero', 'view_tablero'),
        ('lista', 'add_lista'),
        ('lista', 'change_lista'),
        ('lista', 'delete_lista'),
        ('lista', 'view_lista'),
        ('ticket', 'add_ticket'),
        ('ticket', 'change_ticket'),
        ('ticket', 'delete_ticket'),
        ('ticket', 'view_ticket'),
        ('comentario', 'add_comentario'),
        ('comentario', 'change_comentario'),
        ('comentario', 'delete_comentario'),
        ('comentario', 'view_comentario'),
        ('etiqueta', 'add_etiqueta'),
        ('etiqueta', 'change_etiqueta'),
        ('etiqueta', 'delete_etiqueta'),
        ('etiqueta', 'view_etiqueta'),
        ('usuario', 'view_perfilusuario'),
        ('usuario', 'change_perfilusuario'),
    },
    'empleado': {
        ('tablero', 'view_tablero'),
        ('lista', 'view_lista'),
        ('ticket', 'add_ticket'),
        ('ticket', 'change_ticket'),
        ('ticket', 'view_ticket'),
        ('comentario', 'add_comentario'),
        ('comentario', 'change_comentario'),
        ('comentario', 'view_comentario'),
        ('etiqueta', 'view_etiqueta'),
    },
    'cliente': {
        ('tablero', 'view_tablero'),
        ('lista', 'view_lista'),
        ('ticket', 'view_ticket'),
        ('comentario', 'add_comentario'),
        ('comentario', 'view_comentario'),
        ('etiqueta', 'view_etiqueta'),
    },
}


def _role_group_names():
    return list(PerfilUsuario.ROLE_GROUP_MAP.values())


def _sync_group_permissions(group, role_key):
    if role_key == 'admin':
        permissions = Permission.objects.filter(content_type__app_label__in=MANAGED_APPS)
    else:
        permissions = Permission.objects.filter(
            content_type__app_label__in=[app for app, _ in ROLE_PERMISSIONS[role_key]],
            codename__in=[codename for _, codename in ROLE_PERMISSIONS[role_key]],
        )
    group.permissions.set(permissions)


def _sync_user_role_group(*, user, rol):
    role_groups = list(Group.objects.filter(name__in=_role_group_names()))
    user.groups.remove(*role_groups)
    group_name = PerfilUsuario.ROLE_GROUP_MAP[rol]
    group, _ = Group.objects.get_or_create(name=group_name)
    role_key = ROLE_PERMISSION_KEYS[rol]
    _sync_group_permissions(group, role_key)
    user.groups.add(group)


@receiver(post_save, sender=User)
def ensure_perfil_usuario(sender, instance, **kwargs):
    default_role = PerfilUsuario.Rol.ADMIN if instance.is_superuser else PerfilUsuario.Rol.EMPLEADO
    perfil, created = PerfilUsuario.objects.get_or_create(user=instance, defaults={'rol': default_role})
    if not created and instance.is_superuser and perfil.rol != PerfilUsuario.Rol.ADMIN:
        perfil.rol = PerfilUsuario.Rol.ADMIN
        perfil.save(update_fields=['rol'])
        return
    _sync_user_role_group(user=instance, rol=perfil.rol)


@receiver(post_save, sender=PerfilUsuario)
def sync_perfil_role_group(sender, instance, **kwargs):
    _sync_user_role_group(user=instance.user, rol=instance.rol)
