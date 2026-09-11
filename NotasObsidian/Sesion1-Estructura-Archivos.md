---
tags:
  - django
  - estructura
  - archivos
related:
  - DAE-Sesion1
created: 2026-08-28
---

# Sesion1 - Estructura de Archivos

## Mapa completo del proyecto

```
C:\Users\MAGALY\Documents\IV CICLO\DAE\Sesion1\
│
│  .gitignore                  # Excluye: venv/, __pycache__/*.pyc, db.sqlite3
│  db.sqlite3                  # Base de datos SQLite (generada por migraciones)
│  manage.py                   # Script de gestión: runserver, migrate, startapp...
│
├── Sesion1/                   # Paquete de configuración del proyecto Django
│   ├── __init__.py            # Paquete Python vacío
│   ├── settings.py            # Config global: apps, DB, templates, static
│   ├── urls.py                # Router raíz: admin/, core/, calculadora/
│   ├── asgi.py                # Entry point ASGI (servidores asíncronos)
│   └── wsgi.py                # Entry point WSGI (servidores síncronos)
│
├── core/                      # App 1: Home page + Tareas
│   ├── __init__.py            # Paquete vacío
│   ├── admin.py               # (vacío — Task no registrado en admin)
│   ├── apps.py                # CoreConfig — Metadatos de la app
│   ├── models.py              # class Task: title, completed
│   ├── views.py               # home(), task_list()
│   ├── urls.py                # '' → home, 'tareas/' → task_list
│   ├── tests.py               # (boilerplate — vacío)
│   │
│   ├── migrations/
│   │   ├── __init__.py        # Paquete vacío
│   │   └── 0001_initial.py    # Crea tabla core_task (id, title, completed)
│   │
│   ├── static/
│   │   └── core/
│   │       └── css/
│   │           └── styles.css # CSS: navbar, hero, features, footer
│   │
│   └── templates/
│       └── core/
│           ├── home.html      # Landing page: navbar, hero, features, footer
│           └── task_list.html # Extiende home.html + lista de tareas
│
└── calculadora/               # App 2: Calculadora web
    ├── __init__.py            # Paquete vacío
    ├── admin.py               # (vacío)
    ├── apps.py                # CalculadoraConfig
    ├── models.py              # (vacío — no hay modelos)
    ├── views.py               # sumar(), restar(), multiplicar()
    ├── urls.py                # sumar/<a>/<b>, restar/<a>/<b>, multiplicar/<a>/<b>
    └── tests.py               # (boilerplate — vacío)
```

## Resumen de archivos por categoría

### Configuración (3 archivos)

| Archivo | Ubicación | Propósito |
|---------|-----------|-----------|
| `settings.py` | `Sesion1/Sesion1/` | Config global del proyecto |
| `urls.py` (raíz) | `Sesion1/Sesion1/` | Router URL principal |
| `manage.py` | `Sesion1/` | CLI de gestión Django |

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

### App: calculadora (5 archivos)

| Archivo | Ubicación | Propósito |
|---------|-----------|-----------|
| `views.py` | `calculadora/` | sumar(), restar(), multiplicar() |
| `urls.py` | `calculadora/` | Rutas: /app/sumar/*, /app/restar/*, /app/multiplicar/* |
| `apps.py` | `calculadora/` | CalculadoraConfig |
| `models.py` | `calculadora/` | Vacío |
| `admin.py` | `calculadora/` | Vacío |

### Base de datos

| Archivo | Ubicación | Propósito |
|---------|-----------|-----------|
| `db.sqlite3` | `Sesion1/` | Base de datos SQLite |

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
              ├─ GET /tareas/
              │   └── urls.py raíz ──► include('core.urls')
              │                        └── view: task_list()
              │                         └── Task.objects.all()
              │                         └── render: core/task_list.html
              │                         └── Response: 200 OK (HTML)
              │
              ├─ GET /app/sumar/3/5/
              │   └── urls.py raíz ──► include('calculadora.urls')
              │                        └── view: sumar(a=3, b=5)
              │                         └── HttpResponse: "La suma de 3 + 5 = 8"
              │
              ├─ GET /app/restar/10/4/
              │   └── urls.py raíz ──► include('calculadora.urls')
              │                        └── view: restar(a=10, b=4)
              │                         └── HttpResponse: "La resta de 10 - 4 = 6"
              │
              └─ GET /app/multiplicar/6/7/
                  └── urls.py raíz ──► include('calculadora.urls')
                                       └── view: multiplicar(a=6, b=7)
                                        └── HttpResponse: "La multiplicacion de 6 x 7 = 42"
```

## Archivos relacionados

- [[DAE-Sesion1]] — Resumen del proyecto
- [[Sesion1-Configuracion]] — settings.py
- [[Sesion1-URLs-Routing]] — Router
- [[Sesion1-Modelo-Task]] — Modelo
- [[Sesion1-Views-Core]] — Vistas core
- [[Sesion1-Views-Calculadora]] — Vistas calculadora
- [[Sesion1-Templates]] — Templates HTML
