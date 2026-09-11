---
tags:
  - django
  - templates
  - html
  - css
related:
  - Overview-Sesion2
created: 2026-08-28
---

# Sesion2 - Templates

## Estructura

```
Sesion2/core/templates/core/
├── home.html         # Landing page principal
└── task_list.html    # Vista de lista de tareas

Sesion2/core/static/core/css/
└── styles.css        # Estilos CSS
```

## Template: home.html

### Ruta

`Sesion2/core/templates/core/home.html`

### Estructura HTML

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

### Tags de Django Template Language

| Tag | Uso |
|-----|-----|
| `{% static 'core/css/styles.css' %}` | Referencia al archivo CSS estático |
| `{% load static %}` | Carga el tag `{% static %}` |

## Template: task_list.html

### Ruta

`Sesion2/core/templates/core/task_list.html`

### Estructura

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

### Tags de Django Template Language

| Tag | Uso |
|-----|-----|
| `{% for task in tasks %}` | Itera sobre el QuerySet de tareas |
| `{{ task.title }}` | Variable: imprime el título de la tarea |

## CSS: styles.css

### Ruta

`Sesion2/core/static/core/css/styles.css`

### Secciones

- Reset (`*`)
- Body
- Container
- Navbar (sticky, dark bg)
- Hero (gradient blue, centered)
- Features (grid de cards)
- Footer (dark bg)

## Archivos relacionados

- [[Overview-Sesion2]] — Resumen del proyecto
- [[Sesion2-Views-Core]] — Vistas de core
- [[Sesion2-Configuracion]] — settings.py (STATIC_URL, TEMPLATES)
