---
tags:
  - proyecto
  - django
  - web
created: 2026-08-28
status: activo
---

# DAE - Sesion1

Proyecto Django 5.2.17 para la asignatura **DAE** (Desarrollo de Aplicaciones Web), IV Ciclo.

## Resumen

Aplicación web con dos apps autocontenidas:

- **`core`** — Página de inicio + lista de tareas (Task)
- **`calculadora`** — Operaciones aritméticas (sumar, restar, multiplicar) por URL

## Arquitectura

```
DAE/Sesion1/
├── db.sqlite3                          # Base de datos SQLite
├── manage.py                           # Script de gestión Django
├── .gitignore
│
├── Sesion1/                            # Configuración del proyecto
│   ├── __init__.py
│   ├── settings.py                     # Settings: DB, apps, middleware
│   ├── urls.py                         # Router raíz
│   ├── asgi.py                         # Entry ASGI
│   └── wsgi.py                         # Entry WSGI
│
├── core/                               # App 1: Home + Tareas
│   ├── models.py                       # Task(id, title, completed)
│   ├── views.py                        # home(), task_list()
│   ├── urls.py                         # '' → home, 'tareas/' → task_list
│   ├── templates/core/
│   │   ├── home.html                   # Landing page con navbar, hero, features
│   │   └── task_list.html              # Lista de tareas
│   ├── static/core/css/styles.css      # Estilos
│   └── migrations/
│       └── 0001_initial.py             # Creación del modelo Task
│
└── calculadora/                        # App 2: Calculadora
    ├── models.py                       # (vacío)
    ├── views.py                        # sumar(), restar(), multiplicar()
    └── urls.py                         # 'app/sumar/<a>/<b>/', 'app/restar/<a>/<b>/', 'app/multiplicar/<a>/<b>'
```

## Ejecución

```bash
cd Sesion1
python manage.py runserver
```

- Homepage: `http://localhost:8000/`
- Tareas: `http://localhost:8000/tareas/`
- Calculadora: `http://localhost:8000/app/sumar/3/5/`

## Dependencias

| Paquete | Versión | Propósito |
|---------|---------|-----------|
| Django | 5.2.17 | Framework web |
| SQLite3 | (bundled) | Base de datos |

## Base de datos

- Motor: `django.db.backends.sqlite3`
- Archivo: `db.sqlite3` (raíz de Sesion1/)
- Migraciones: Django Migrations
- AutoField por defecto: `BigAutoField`

## Archivos relacionados

- [[Sesion1-Configuracion]] — settings.py, variables, apps instaladas
- [[Sesion1-URLs-Routing]] — Router raíz y sub-aplicaciones
- [[Sesion1-Modelo-Task]] — Modelo Task, campos, migración
- [[Sesion1-Views-Core]] — Vistas de la app core
- [[Sesion1-Views-Calculadora]] — Vistas de la app calculadora
- [[Sesion1-Templates]] — Templates HTML y CSS
- [[Sesion1-Estructura-Archivos]] — Mapa detallado de archivos
