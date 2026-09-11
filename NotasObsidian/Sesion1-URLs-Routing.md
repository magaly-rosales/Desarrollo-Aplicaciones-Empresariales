---
tags:
  - django
  - urls
  - routing
related:
  - DAE-Sesion1
created: 2026-08-28
---

# Sesion1 - URLs & Routing

## Router Raíz

Archivo: `Sesion1/Sesion1/urls.py`

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('app/', include('calculadora.urls')),
]
```

## App: core

Archivo: `Sesion1/core/urls.py`

| Patrón | Vista | Nombre | URL completa |
|--------|-------|--------|--------------|
| `''` (root) | `home` | `home` | `/` |
| `tareas/` | `task_list` | `task_list` | `/tareas/` |

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tareas/', views.task_list, name='task_list'),
]
```

## App: calculadora

Archivo: `Sesion1/calculadora/urls.py`

| Patrón | Vista | Nombre | URL completa |
|--------|-------|--------|--------------|
| `sumar/<int:a>/<int:b>/` | `sumar` | `sumar` | `/app/sumar/3/5/` |
| `restar/<int:a>/<int:b>/` | `restar` | `restar` | `/app/restar/10/4/` |
| `multiplicar/<int:a>/<int:b>/` | `multiplicar` | `multiplicar` | `/app/multiplicar/6/7/` |

```python
from django.urls import path
from . import views

urlpatterns = [
    path('sumar/<int:a>/<int:b>/', views.sumar, name='sumar'),
    path('restar/<int:a>/<int:b>/', views.restar, name='restar'),
    path('multiplicar/<int:a>/<int:b>/', views.multiplicar, name='multiplicar'),
]
```

## Diagrama de routing

```
Request URL
    │
    ├─ admin/ ──────────► Django Admin (built-in)
    │
    ├─ (root) ─────────► core.urls
    │       │
    │       ├─ '' ──────► views.home() → core/home.html
    │       │
    │       └─ 'tareas/' ──► views.task_list() → core/task_list.html
    │
    └─ app/ ───────────► calculadora.urls
            │
            ├─ 'sumar/<a>/<b>/' ──► views.sumar(a, b) → plain text
            │
            ├─ 'restar/<a>/<b>/' ──► views.restar(a, b) → plain text
            │
            └─ 'multiplicar/<a>/<b>/' ──► views.multiplicar(a, b) → plain text
```

## Archivos relacionados

- [[DAE-Sesion1]] — Resumen del proyecto
- [[Sesion1-Configuracion]] — settings.py
- [[Sesion1-Views-Core]] — Vistas de core
- [[Sesion1-Views-Calculadora]] — Vistas de calculadora
