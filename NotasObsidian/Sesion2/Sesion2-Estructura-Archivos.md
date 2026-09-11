---
tags:
  - django
  - estructura
  - archivos
related:
  - Overview-Sesion2
created: 2026-08-28
---

# Sesion2 - Estructura de Archivos

## Mapa completo del proyecto

```
Sesion2/
│
│  .gitignore                  # Excluye: venv/, __pycache__/*.pyc, db.sqlite3
│  db.sqlite3                  # Base de datos SQLite (generada por migraciones)
│  manage.py                   # Script de gestión: runserver, migrate, startapp...
│
├── Sesion2/                   # Paquete de configuración del proyecto Django
│   ├── __init__.py            # Paquete Python vacío
│   ├── settings.py            # Config global: apps, DB, templates, static
│   ├── urls.py                # Router raíz: admin/, core/
│   ├── asgi.py                # Entry point ASGI (servidores asíncronos)
│   └── wsgi.py                # Entry point WSGI (servidores síncronos)
│
└── core/                      # App: Home page + Tareas
    ├── __init__.py            # Paquete vacío
    ├── admin.py               # (vacío — Task no registrado en admin)
    ├── apps.py                # CoreConfig — Metadatos de la app
    ├── models.py              # class Task: title, completed
    ├── views.py               # home(), task_list()
    ├── urls.py                # '' → home, 'tareas/' → task_list
    ├── tests.py               # (boilerplate — vacío)
    │
    ├── migrations/
    │   ├── __init__.py        # Paquete vacío
    │   └── 0001_initial.py    # Crea tabla core_task (id, title, completed)
    │
    ├── static/
    │   └── core/
    │       └── css/
    │           └── styles.css # CSS: navbar, hero, features, footer
    │
    └── templates/
        └── core/
            ├── home.html      # Landing page: navbar, hero, features, footer
            └── task_list.html # Lista de tareas
```

## Resumen de archivos por categoría

### Configuración (5 archivos)

| Archivo | Ubicación | Propósito |
|---------|-----------|-----------|
| `settings.py` | `Sesion2/Sesion2/` | Config global del proyecto |
| `urls.py` (raíz) | `Sesion2/Sesion2/` | Router URL principal |
| `asgi.py` | `Sesion2/Sesion2/` | Entry ASGI |
| `wsgi.py` | `Sesion2/Sesion2/` | Entry WSGI |
| `manage.py` | `Sesion2/` | CLI de gestión Django |

### App: core (9 archivos + 1 migración + 1 CSS + 2 templates)

| Archivo | Ubicación | Propósito |
|---------|-----------|-----------|
| `models.py` | `core/` | Modelo Task |
| `views.py` | `core/` | home(), task_list() |
| `urls.py` | `core/` | Rutas: /, /tareas/ |
| `apps.py` | `core/` | CoreConfig |
| `admin.py` | `core/` | Vacío |
| `tests.py` | `core/` | Boilerplate vacío |
| `__init__.py` | `core/` | Paquete |
| `0001_initial.py` | `core/migrations/` | Creación de Task |
| `styles.css` | `core/static/core/css/` | Estilos CSS |
| `home.html` | `core/templates/core/` | Landing page |
| `task_list.html` | `core/templates/core/` | Lista de tareas |

### Base de datos

| Archivo | Ubicación | Propósito |
|---------|-----------|-----------|
| `db.sqlite3` | `Sesion2/` | Base de datos SQLite |

## Flujo de request-response completo

```
Cliente ──► Request URL
              │
              ├─ GET /
              │   └── urls.py raíz ──► include('core.urls')
              │                        └── view: home()
              │                         └── render: core/home.html
              │                         └── Response: 200 OK (HTML)
              │
              └─ GET /tareas/
                  └── urls.py raíz ──► include('core.urls')
                                       └── view: task_list()
                                        └── Task.objects.all()
                                        └── render: core/task_list.html
                                        └── Response: 200 OK (HTML)
```

## Archivos relacionados

- [[Overview-Sesion2]] — Resumen del proyecto
- [[Sesion2-Configuracion]] — settings.py
- [[Sesion2-URLs-Routing]] — Router
- [[Sesion2-Modelo-Task]] — Modelo
- [[Sesion2-Views-Core]] — Vistas core
- [[Sesion2-Templates]] — Templates HTML
