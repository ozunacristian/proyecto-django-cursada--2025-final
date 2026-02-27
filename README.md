# Gestor Castor - Tickets para Mantenimiento Integral

Aplicacion MVP web desarrollada en Django para gestionar tableros Kanban, listas y tickets en un contexto de mantenimiento integral (hospitales, consorcios, plantas, etc.).

El sistema contempla:
- gestion de tableros por equipos,
- flujo de tickets por columnas,
- comentarios por ticket,
- etiquetas por tablero,
- permisos por rol y visibilidad por pertenencia.

## Stack Tecnologico

- Python 3.x
- Django 6.x
- SQLite (entorno local)
- Bootstrap 5

## Estructura Funcional

- `apps/tablero`: tableros e integrantes.
- `apps/lista`: columnas del tablero.
- `apps/ticket`: ciclo de vida del ticket.
- `apps/comentario`: comentarios por ticket.
- `apps/etiqueta`: etiquetas y relacion etiqueta-ticket.
- `apps/usuario`: login, perfil, roles, permisos y sincronizacion de grupos.

## Roles y Permisos

Roles disponibles:
- `admin`
- `supervisor`
- `empleado`
- `cliente`

La autorizacion se implementa con:
- `PermissionRequiredMixin` en vistas,
- visibilidad por pertenencia usando `tableros_visibles_para_usuario(...)`,
- sincronizacion automatica de grupos/permisos mediante `signals`.

## Requisitos Previos

Tener instalado:
- Python 3.11+ (recomendado),
- `pip`,
- entorno virtual (`venv`).

## Instalacion y Ejecucion

1. Clonar repositorio:
```bash
git clone https://github.com/ozunacristian/proyecto-django-cursada--2025-final.git
Ingresar a directorio
```

2. Crear y activar entorno virtual:
```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Aplicar migraciones:
```bash
python manage.py migrate
```

5. Crear superusuario:
```bash
python manage.py createsuperuser
```

6. Levantar servidor:
```bash
python manage.py runserver
```

## Carga de Datos Demo (seed)

El proyecto incluye un comando de carga inicial para demostracion:

```bash
python manage.py seed_demo
```

Este comando crea:
- usuarios por rol,
- tableros de ejemplo,
- listas por tablero,
- tickets,
- comentarios,
- etiquetas y sus relaciones.

Credenciales demo:
- `admin_demo` / `Admin123!` / `admin@demo.com.ar`

- resto de usuarios demo: 
- `sup_ana` / `Demo123!` (supervisor)
- `sup_marcos` / `Demo123!` (supervisor)
- `emp_lucia` / `Demo123!` (empleado)
- `emp_tomas` / `Demo123!` (empleado)
- `cli_hospital` / `Demo123!` (cliente)
- `cli_consorcio` / `Demo123!` (cliente)

Nota: la funcionalidad de asignacion de responsable en formulario fue deshabilitada en esta version. Los tickets del seed se crean sin `asignado_a`.

## Reset Limpio (DB + migraciones propias)

Uso recomendado para demo local:

1. Detener `runserver`.
2. Borrar DB local:
```bash
del gestor_castor_db.sqlite3
```
3. Borrar migraciones de apps propias (excepto `__init__.py`).
4. Regenerar:
```bash
python manage.py makemigrations
python manage.py migrate
```
5. Crear superusuario y volver a cargar demo:
```bash
python manage.py createsuperuser
python manage.py seed_demo
```

## Flujo Principal de Uso

1. Login.
2. Ingreso a tablero.
3. Creacion de ticket desde una lista.
4. Movimiento rapido entre listas con dropdown `Mover`.
5. Comentarios en ticket.
6. Etiquetas en ticket.
7. Busqueda por titulo/descripcion dentro del tablero.

## Comandos Utiles

Chequeo general:
```bash
python manage.py check
```

Compilacion rapida de sintaxis:
```bash
python -m py_compile apps/tablero/views.py apps/ticket/views.py
```

## Estado del Proyecto

Version para demo con:
- permisos por rol funcionales,
- flujo Kanban operativo,
- comentarios y etiquetas integrados,
- buscador server-side por ticket (aún en desarrollo),
- seed reproducible.

### Proyecto desarrollado para la cursada final de la materia BackEnd 2025.

