---
tags:
  - django
  - modelos
  - base-datos
related:
  - DAE-Sesion1
created: 2026-08-28
---

# Sesion1 - Modelo Task (app core)

## Ruta

`Sesion1/core/models.py`

## Modelo: Task

```python
from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
```

## Campos

| Campo | Tipo | Valor por defecto | Restricciones |
|-------|------|-------------------|---------------|
| `id` | `BigAutoField` (PK, auto) | Auto-generated | Primary Key |
| `title` | `CharField` | — | `max_length=200` |
| `completed` | `BooleanField` | `False` | — |

## Métodos

- **`__str__(self)`**: Retorna `self.title` (se muestra en admin y shell de Django)

## Migración

Archivo: `Sesion1/core/migrations/0001_initial.py`

- Fecha: 2026-08-21
- Crea la tabla `core_task` con campos `id`, `title`, `completed`
- `completed` tiene valor por defecto `False`
- No hay foreign keys ni relaciones

## Uso en View

Archivo: `Sesion1/core/views.py`

```python
from .models import Task

def task_list(request):
    tareas = Task.objects.all()
    return render(request, 'core/task_list.html', {'tareas': tareas})
```

- Fetch all tasks: `Task.objects.all()`
- Pasa la query a `task_list.html` como variable `tareas`

## Diagrama de datos

```
┌───────────── core_task ─────────────┐
│ id (BigAutoField, PK, auto)         │
│ title  (CharField, max_length=200)  │
│ completed(BooleanField, default=F)  │
└─────────────────────────────────────┘
```

## Archivos relacionados

- [[DAE-Sesion1]] — Resumen del proyecto
- [[Sesion1-Views-Core]] — Vistas de core
- [[Sesion1-URLs-Routing]] — Router
