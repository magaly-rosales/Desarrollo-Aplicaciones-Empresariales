---
tags:
  - proyecto
  - django
  - web
created: 2026-08-28
status: activo
---

# Sesion2

Proyecto Django 5.2.17 para la asignatura **DAE** (Desarrollo de Aplicaciones Web), IV Ciclo.

## Resumen

Aplicación web con una sola app:

- **`core`** — Página de inicio (landing) + lista de tareas (Task)

## Arquitectura

```
Sesion2/
├── db.sqlite3                          # Base de datos SQLite
├── manage.py                           # Script de gestión Django
├── .gitignore
│
├── Sesion2/                            # Configuración del proyecto
│   ├── __init__.py
│   ├── settings.py                     # Settings: DB, apps, middleware
│   ├── urls.py                         # Router raíz
│   ├── asgi.py                         # Entry ASGI
│   └── wsgi.py                         # Entry WSGI
│
└── core/                               # App: Home + Tareas
    ├── models.py                       # Task(id, title, completed)
    ├── views.py                        # home(), task_list()
    ├── urls.py                         # '' → home, 'tareas/' → task_list
    ├── templates/core/
    │   ├── home.html                   # Landing page con navbar, hero, features
    │   └── task_list.html              # Lista de tareas
    ├── static/core/css/styles.css      # Estilos
    ├── migrations/
    │   └── 0001_initial.py             # Creación del modelo Task
    ├── admin.py                        # (vacío)
    └── tests.py                        # (boilerplate)
```

## Ejecución

```bash
cd Sesion2
python manage.py runserver
```

- Homepage: `http://localhost:8000/`
- Tareas: `http://localhost:8000/tareas/`

## Dependencias

| Paquete | Versión | Propósito |
|---------|---------|-----------|
| Django | 5.2.17 | Framework web |
| SQLite3 | (bundled) | Base de datos |

## Archivos relacionados

- [[Sesion2-Configuracion]] — settings.py, variables, apps instaladas
- [[Sesion2-URLs-Routing]] — Router raíz y sub-aplicaciones
- [[Sesion2-Modelo-Task]] — Modelo Task, campos, migración
- [[Sesion2-Views-Core]] — Vistas de la app core
- [[Sesion2-Templates]] — Templates HTML y CSS
- [[Sesion2-Estructura-Archivos]] — Mapa detallado de archivos
