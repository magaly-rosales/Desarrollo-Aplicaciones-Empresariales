---
tags:
  - django
  - urls
  - routing
related:
  - Overview-Sesion2
created: 2026-08-28
---

# Sesion2 - URLs & Routing

## Router Raíz

Archivo: `Sesion2/Sesion2/urls.py`

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]
```

## App: core

Archivo: `Sesion2/core/urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tareas/', views.task_list, name='task_list'),
]
```

| Patrón | Vista | Nombre | URL completa |
|--------|-------|--------|--------------|
| `''` (root) | `home` | `home` | `/` |
| `tareas/` | `task_list` | `task_list` | `/tareas/` |

## Diagrama de routing

```
Request URL
    │
    ├─ admin/ ──────────► Django Admin (built-in)
    │
    └─ (root) ─────────► core.urls
            │
            ├─ '' ──────► views.home() → core/home.html
            │
            └─ 'tareas/' ──► views.task_list() → core/task_list.html
```

## Archivos relacionados

- [[Overview-Sesion2]] — Resumen del proyecto
- [[Sesion2-Configuracion]] — settings.py
- [[Sesion2-Views-Core]] — Vistas de core
