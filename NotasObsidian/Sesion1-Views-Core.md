---
tags:
  - django
  - vistas
  - core
related:
  - DAE-Sesion1
created: 2026-08-28
---

# Sesion1 - Views Core (app core)

## Ruta

`Sesion1/core/views.py`

## Vista: home

```python
from django.shortcuts import render

def home(request):
    return render(request, 'core/home.html')
```

- **URL**: `/` (ruta vacía, raíz del sitio)
- **Método**: Solo `GET`
- **Template**: `core/home.html`
- **Contexto**: Vacío — no pasa datos al template
- **Propósito**: Página de aterrizaje con navbar, hero section, features grid, footer

### Template: home.html

```html
<!-- core/templates/core/home.html -->
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DAE - Sesion1</title>
    <link rel="stylesheet" href="{% static 'core/css/styles.css' %}">
</head>
<body>
    <!-- Navbar -->
    <nav>...</nav>
    
    <!-- Hero Section -->
    <section class="hero">
        <h1>DAE - Sesion1</h1>
        <p>Desarrollo de Aplicaciones Web</p>
    </section>
    
    <!-- Features Grid -->
    <section class="features">
        <div class="feature">
            <h2>Tareas</h2>
            <a href="{% url 'task_list' %}">Ver tareas →</a>
        </div>
        <div class="feature">
            <h2>Calculadora</h2>
            <a href="/app/sumar/3/5/">Probar calculadora →</a>
        </div>
    </section>
    
    <!-- Footer -->
    <footer>
        <p>2026 Sesion1 - IV Ciclo | DAE</p>
    </footer>
</body>
</html>
```

## Vista: task_list

```python
from .models import Task

def task_list(request):
    tareas = Task.objects.all()
    return render(request, 'core/task_list.html', {'tareas': tareas})
```

- **URL**: `/tareas/`
- **Método**: Solo `GET`
- **Template**: `core/task_list.html`
- **Contexto**: `{'tareas': <QuerySet de Task>}`
- **Propósito**: Listar todas las tareas de la base de datos
- **Lógica de negocio**: Fetch `Task.objects.all()` — sin filtrado, sin paginación

### Template: task_list.html

```html
<!-- core/templates/core/task_list.html -->
<!-- Extiende de home.html o incluye template base -->
{% extends 'core/home.html' %}

{% block content %}
<h2>Lista de Tareas</h2>
<ul>
    {% for tarea in tareas %}
        <li>
            {% if tarea.completed %}
                ✅ {{ tarea.title }}
            {% else %}
                ⬜ {{ tarea.title }}
            {% endif %}
        </li>
    {% empty %}
        <li>No hay tareas.</li>
    {% endfor %}
</ul>
{% endblock %}
```

## Flujo de datos: core

```
Request: GET /
    │
    ▼
home(request)
    │
    ├── render('core/home.html')
    │
    └── Response: HTML con navbar, hero, features, footer


Request: GET /tareas/
    │
    ▼
task_list(request)
    │
    ├── Task.objects.all() → QuerySet [Task1, Task2, ...]
    │
    ├── render('core/task_list.html', {'tareas': <QuerySet>})
    │
    └── Response: HTML con lista de tareas renderizada
```

## Archivos relacionados

- [[DAE-Sesion1]] — Resumen del proyecto
- [[Sesion1-URLs-Routing]] — Router
- [[Sesion1-Modelo-Task]] — Modelo Task
- [[Sesion1-Templates]] — Templates HTML
