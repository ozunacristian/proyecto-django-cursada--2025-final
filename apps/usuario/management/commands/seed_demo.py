from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.comentario.models import Comentario
from apps.etiqueta.models import Etiqueta, EtiquetaTicket
from apps.lista.models import Lista
from apps.tablero.models import IntegranteTablero, Tablero
from apps.ticket.models import Ticket
from apps.usuario.models import PerfilUsuario

User = get_user_model()


USERS = [
    {
        'username': 'admin_demo',
        'email': 'admin@demo.com.ar',
        'password': 'Admin123!',
        'rol': PerfilUsuario.Rol.ADMIN,
        'is_superuser': True,
        'is_staff': True,
    },
    {
        'username': 'sup_ana',
        'email': 'ana.supervisor@demo.com.ar',
        'password': 'Demo123!',
        'rol': PerfilUsuario.Rol.SUPERVISOR,
        'is_superuser': False,
        'is_staff': True,
    },
    {
        'username': 'sup_marcos',
        'email': 'marcos.supervisor@demo.com.ar',
        'password': 'Demo123!',
        'rol': PerfilUsuario.Rol.SUPERVISOR,
        'is_superuser': False,
        'is_staff': True,
    },
    {
        'username': 'emp_lucia',
        'email': 'lucia.empleado@demo.com.ar',
        'password': 'Demo123!',
        'rol': PerfilUsuario.Rol.EMPLEADO,
        'is_superuser': False,
        'is_staff': False,
    },
    {
        'username': 'emp_tomas',
        'email': 'tomas.empleado@demo.com.ar',
        'password': 'Demo123!',
        'rol': PerfilUsuario.Rol.EMPLEADO,
        'is_superuser': False,
        'is_staff': False,
    },
    {
        'username': 'cli_hospital',
        'email': 'hospital.cliente@demo.com.ar',
        'password': 'Demo123!',
        'rol': PerfilUsuario.Rol.CLIENTE,
        'is_superuser': False,
        'is_staff': False,
    },
    {
        'username': 'cli_consorcio',
        'email': 'consorcio.cliente@demo.com.ar',
        'password': 'Demo123!',
        'rol': PerfilUsuario.Rol.CLIENTE,
        'is_superuser': False,
        'is_staff': False,
    },
]


BOARD_LISTS = [
    (1, 'Pendientes'),
    (2, 'En curso'),
    (3, 'Esperando repuesto'),
    (4, 'Verificacion'),
    (5, 'Cerrados'),
]


BOARDS = [
    {
        'titulo': 'Hospital San Gabriel - Mantenimiento',
        'descripcion': 'Incidencias y tareas tecnicas del edificio hospitalario.',
        'creado_por': 'sup_ana',
        'integrantes': ['sup_ana', 'emp_lucia', 'emp_tomas', 'cli_hospital'],
    },
    {
        'titulo': 'Consorcio Torre Norte - Mantenimiento',
        'descripcion': 'Seguimiento operativo de reclamos del consorcio.',
        'creado_por': 'sup_marcos',
        'integrantes': ['sup_marcos', 'emp_tomas', 'cli_consorcio'],
    },
    {
        'titulo': 'Planta Industrial Delta - Preventivo',
        'descripcion': 'Planificacion de mantenimiento preventivo industrial.',
        'creado_por': 'sup_ana',
        'integrantes': ['sup_ana', 'emp_lucia'],
    },
]


TICKETS = [
    {
        'tablero': 'Hospital San Gabriel - Mantenimiento',
        'lista_orden': 1,
        'titulo': 'Fuga en caneria sala 3',
        'descripcion': 'Cliente reporta goteo continuo en pared lateral.',
        'prioridad': 3,
        'creado_por': 'cli_hospital',
    },
    {
        'tablero': 'Hospital San Gabriel - Mantenimiento',
        'lista_orden': 2,
        'titulo': 'Tablero electrico pasillo B',
        'descripcion': 'Se detecta olor a quemado al energizar el sector.',
        'prioridad': 3,
        'creado_por': 'sup_ana',
    },
    {
        'tablero': 'Hospital San Gabriel - Mantenimiento',
        'lista_orden': 3,
        'titulo': 'Cambio de luminarias UTI',
        'descripcion': 'Quedaron pendientes 4 artefactos por falta de stock.',
        'prioridad': 2,
        'creado_por': 'emp_lucia',
    },
    {
        'tablero': 'Hospital San Gabriel - Mantenimiento',
        'lista_orden': 4,
        'titulo': 'Ajuste puerta automatica guardia',
        'descripcion': 'Puerta recalibrada, se solicita verificacion final.',
        'prioridad': 1,
        'creado_por': 'emp_tomas',
    },
    {
        'tablero': 'Consorcio Torre Norte - Mantenimiento',
        'lista_orden': 1,
        'titulo': 'Bomba de agua con ruido',
        'descripcion': 'Ruido metalico en arranque durante horario pico.',
        'prioridad': 3,
        'creado_por': 'cli_consorcio',
    },
    {
        'tablero': 'Consorcio Torre Norte - Mantenimiento',
        'lista_orden': 2,
        'titulo': 'Porton cochera no cierra',
        'descripcion': 'El sensor no detecta fin de carrera correctamente.',
        'prioridad': 2,
        'creado_por': 'sup_marcos',
    },
    {
        'tablero': 'Consorcio Torre Norte - Mantenimiento',
        'lista_orden': 5,
        'titulo': 'Revision matafuegos piso 9',
        'descripcion': 'Control anual completado y registrado.',
        'prioridad': 1,
        'creado_por': 'emp_tomas',
    },
    {
        'tablero': 'Planta Industrial Delta - Preventivo',
        'lista_orden': 1,
        'titulo': 'Vibracion anormal en compresor 2',
        'descripcion': 'Se recomienda detener equipo hasta inspeccion.',
        'prioridad': 3,
        'creado_por': 'sup_ana',
    },
    {
        'tablero': 'Planta Industrial Delta - Preventivo',
        'lista_orden': 2,
        'titulo': 'Mantenimiento preventivo cinta A',
        'descripcion': 'Engrase y ajuste planificado en turno manana.',
        'prioridad': 2,
        'creado_por': 'emp_lucia',
    },
    {
        'tablero': 'Planta Industrial Delta - Preventivo',
        'lista_orden': 3,
        'titulo': 'Sensor de temperatura intermitente',
        'descripcion': 'Se solicito repuesto por lectura fuera de rango.',
        'prioridad': 2,
        'creado_por': 'emp_lucia',
    },
]


LABELS = [
    ('Urgente', '#dc3545'),
    ('Electrico', '#0d6efd'),
    ('Plomeria', '#20c997'),
    ('Seguridad', '#ffc107'),
    ('Repuestos', '#6c757d'),
]


TICKET_LABELS = [
    ('Fuga en caneria sala 3', ['Urgente', 'Plomeria']),
    ('Tablero electrico pasillo B', ['Urgente', 'Electrico']),
    ('Cambio de luminarias UTI', ['Electrico', 'Repuestos']),
    ('Bomba de agua con ruido', ['Urgente', 'Seguridad']),
    ('Sensor de temperatura intermitente', ['Repuestos', 'Seguridad']),
]


COMMENTS = [
    ('Fuga en caneria sala 3', 'cli_hospital', 'Detectamos humedad desde anoche en el sector.'),
    ('Fuga en caneria sala 3', 'sup_ana', 'Recibido. Se asigna inspeccion en la primera franja del dia.'),
    ('Tablero electrico pasillo B', 'emp_tomas', 'Se aislou el circuito y quedo en condicion segura.'),
    ('Porton cochera no cierra', 'cli_consorcio', 'Ocurre principalmente entre las 19 y las 21 hs.'),
    ('Sensor de temperatura intermitente', 'emp_lucia', 'Se verifico cableado y se gestiono compra de sensor nuevo.'),
]


class Command(BaseCommand):
    help = 'Carga datos demo para la aplicacion de gestion de tickets.'

    def handle(self, *args, **options):
        users_by_username = self._seed_users()
        boards_by_title = self._seed_boards(users_by_username)
        lists_by_key = self._seed_lists(boards_by_title)
        tickets_by_title = self._seed_tickets(users_by_username, boards_by_title, lists_by_key)
        self._seed_labels(boards_by_title)
        self._seed_ticket_labels(boards_by_title, tickets_by_title)
        self._seed_comments(users_by_username, tickets_by_title)

        self.stdout.write(self.style.SUCCESS('Seed demo completado correctamente.'))
        self.stdout.write('Usuarios: {}'.format(User.objects.count()))
        self.stdout.write('Tableros: {}'.format(Tablero.objects.count()))
        self.stdout.write('Listas: {}'.format(Lista.objects.count()))
        self.stdout.write('Tickets: {}'.format(Ticket.objects.count()))
        self.stdout.write('Comentarios: {}'.format(Comentario.objects.count()))
        self.stdout.write('Etiquetas: {}'.format(Etiqueta.objects.count()))
        self.stdout.write('Relaciones ticket-etiqueta: {}'.format(EtiquetaTicket.objects.count()))

    def _seed_users(self):
        users_by_username = {}
        for item in USERS:
            user, _ = User.objects.get_or_create(
                username=item['username'],
                defaults={'email': item['email']},
            )
            user.email = item['email']
            user.is_superuser = item['is_superuser']
            user.is_staff = item['is_staff']
            user.set_password(item['password'])
            user.save()

            perfil, _ = PerfilUsuario.objects.get_or_create(user=user)
            perfil.rol = item['rol']
            perfil.save()
            users_by_username[user.username] = user
        return users_by_username

    def _seed_boards(self, users_by_username):
        boards_by_title = {}
        for item in BOARDS:
            tablero, _ = Tablero.objects.update_or_create(
                titulo=item['titulo'],
                defaults={
                    'descripcion': item['descripcion'],
                    'creado_por': users_by_username[item['creado_por']],
                },
            )
            for username in item['integrantes']:
                IntegranteTablero.objects.get_or_create(
                    usuario=users_by_username[username],
                    tablero=tablero,
                )
            boards_by_title[tablero.titulo] = tablero
        return boards_by_title

    def _seed_lists(self, boards_by_title):
        lists_by_key = {}
        for tablero in boards_by_title.values():
            for orden, titulo in BOARD_LISTS:
                lista, _ = Lista.objects.update_or_create(
                    tablero=tablero,
                    orden=orden,
                    defaults={'titulo': titulo},
                )
                lists_by_key[(tablero.titulo, orden)] = lista
        return lists_by_key

    def _seed_tickets(self, users_by_username, boards_by_title, lists_by_key):
        tickets_by_title = {}
        for item in TICKETS:
            tablero = boards_by_title[item['tablero']]
            lista = lists_by_key[(item['tablero'], item['lista_orden'])]
            ticket, _ = Ticket.objects.update_or_create(
                tablero=tablero,
                titulo=item['titulo'],
                defaults={
                    'descripcion': item['descripcion'],
                    'lista': lista,
                    'creado_por': users_by_username[item['creado_por']],
                    # Feature intencionalmente desactivada en UI actual:
                    # dejamos tickets sin asignar por defecto en la demo.
                    'asignado_a': None,
                    'prioridad': item['prioridad'],
                    'activo': True,
                },
            )
            tickets_by_title[ticket.titulo] = ticket
        return tickets_by_title

    def _seed_labels(self, boards_by_title):
        for tablero in boards_by_title.values():
            for nombre, color in LABELS:
                Etiqueta.objects.update_or_create(
                    tablero=tablero,
                    nombre=nombre,
                    defaults={'color': color},
                )

    def _seed_ticket_labels(self, boards_by_title, tickets_by_title):
        for ticket_title, label_names in TICKET_LABELS:
            ticket = tickets_by_title[ticket_title]
            for label_name in label_names:
                etiqueta = Etiqueta.objects.get(tablero=ticket.tablero, nombre=label_name)
                EtiquetaTicket.objects.get_or_create(ticket=ticket, etiqueta=etiqueta)

    def _seed_comments(self, users_by_username, tickets_by_title):
        for ticket_title, username, contenido in COMMENTS:
            Comentario.objects.get_or_create(
                ticket=tickets_by_title[ticket_title],
                usuario=users_by_username[username],
                contenido=contenido,
            )
