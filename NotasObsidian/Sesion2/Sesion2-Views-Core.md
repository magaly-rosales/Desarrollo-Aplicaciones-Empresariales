---
tags:
  - django
  - vistas
  - core
related:
  - Overview-Sesion2
created: 2026-08-28
---

# Sesion2 - Views Core (app core)

## Ruta

`Sesion2/core/views.py`

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
{% load static %}
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sesion2 - Inicio</title>
    <link rel="stylesheet" href="{% static 'core/css/styles.css' %}">
</head>
<body>
    <!-- Navbar -->
    <header class="navbar">
        <div class="container nav-content">
            <a href="/" class="logo">Sesion<span>2</span></a>
            <nav>
                <a href="#inicio">Inicio</a>
                <a href="#caracteristicas">Características</a>
                <a href="#contacto">Contacto</a>
            </nav>
        </div>
    </header>

    <!-- Hero Section -->
    <section id="inicio" class="hero">
        <div class="container">
            <h1>Bienvenido a <span class="highlight">Sesion2</span></h1>
            <p class="subtitle">Tu primer proyecto con Django. Simple, rápido y potente.</p>
            <a href="#caracteristicas" class="btn">Descubre más</a>
        </div>
    </section>

    <!-- Features Grid -->
    <section id="caracteristicas" class="features">
        <div class="container">
            <h2>Características</h2>
            <div class="grid">
                <div class="card">
                    <h3>⚡ Rápido</h3>
                    <p>Desarrollo ágil con Django y su arquitectura MTV.</p>
                </div>
                <div class="card">
                    <h3>🔒 Seguro</h3>
                    <p>Protección integrada contra CSRF, XSS y SQL Injection.</p>
                </div>
                <div class="card">
                    <h3>📦 Escalable</h3>
                    <p>Estructura modular lista para crecer.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer id="contacto">
        <div class="container">
            <p>&copy; 2026 Sesion2 - IV Ciclo | DAE</p>
        </div>
    </footer>
</body>
</html>
```

## Vista: task_list

```python
from .models import Task

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'core/task_list.html', {'tasks': tasks})
```

- **URL**: `/tareas/`
- **Método**: Solo `GET`
- **Template**: `core/task_list.html`
- **Contexto**: `{'tasks': <QuerySet de Task>}`
- **Propósito**: Listar todas las tareas de la base de datos
- **Lógica de negocio**: Fetch `Task.objects.all()` — sin filtrado, sin paginación

### Template: task_list.html

```html
<!DOCTYPE html>
<html>
<head>
    <title>ToDo List</title>
</head>
<body>
    <h1>Tasks</h1>
    <ul>
        {% for task in tasks %}
        <li>{{ task.title }}</li>
        {% endfor %}
    </ul>
</body>
</html>
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
    ├── render('core/task_list.html', {'tasks': <QuerySet>})
    │
    └── Response: HTML con lista de tareas renderizada
```

## Archivos relacionados

- [[Overview-Sesion2]] — Resumen del proyecto
- [[Sesion2-URLs-Routing]] — Router
- [[Sesion2-Modelo-Task]] — Modelo Task
- [[Sesion2-Templates]] — Templates HTML
