---
tags:
  - django
  - templates
  - html
  - css
related:
  - DAE-Sesion1
created: 2026-08-28
---

# Sesion1 - Templates

## Estructura

```
Sesion1/core/templates/core/
├── home.html         # Landing page principal
└── task_list.html    # Vista de lista de tareas

Sesion1/core/static/core/css/
└── styles.css        # Estilos CSS
```

## Template: home.html

### Ruta

`Sesion1/core/templates/core/home.html`

### Estructura HTML

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DAE - Sesion1</title>
    <link rel="stylesheet" href="{% static 'core/css/styles.css' %}">
</head>
<body>
    <!-- Navbar: links a home y tareas -->
    <nav>
        <a href="{% url 'home' %}">DAE Sesion1</a>
        <a href="{% url 'task_list' %}">Tareas</a>
    </nav>
    
    <!-- Hero Section: título y descripción -->
    <section class="hero">
        <h1>DAE - Sesion1</h1>
        <p>Desarrollo de Aplicaciones Web</p>
    </section>
    
    <!-- Features Grid: dos cards (Tareas y Calculadora) -->
    <section class="features">
        <!-- Card 1: Tareas -->
        <div class="feature">
            <h2>Tareas</h2>
            <a href="{% url 'task_list' %}">Ver tareas →</a>
        </div>
        
        <!-- Card 2: Calculadora -->
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

### Tags de Django Template Language

| Tag | Uso |
|-----|-----|
| `{% static 'core/css/styles.css' %}` | Referencia al archivo CSS estático |
| `{% url 'home' %}` | Reverse URL name → `/` |
| `{% url 'task_list' %}` | Reverse URL name → `/tareas/` |
| `{% load static %}` | Carga el tag `{% static %}` (implícito) |

## Template: task_list.html

### Ruta

`Sesion1/core/templates/core/task_list.html`

### Estructura

```html
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

### Tags de Django Template Language

| Tag | Uso |
|-----|-----|
| `{% extends 'core/home.html' %}` | Extiende el template base (home.html) |
| `{% block content %}` | Sobrescribe/añade contenido en un bloque |
| `{% for tarea in tareas %}` | Itera sobre el QuerySet de tareas |
| `{% if tarea.completed %}` | Condicional: tarea completada o no |
| `{% empty %}` | Si el QuerySet está vacío |
| `{{ tarea.title }}` | Variable: imprime el título de la tarea |

## CSS: styles.css

### Ruta

`Sesion1/core/static/core/css/styles.css`

### Propósito

Estiliza la landing page: navbar, hero, features grid, footer.

## Diagrama de templates

```
home.html (base)
├── <nav> — Navbar con links
├── <section.hero> — Hero section
├── <section.features> — Features grid (2 cards)
└── <footer> — Footer

task_list.html
├── {% extends 'core/home.html' %} — Hereda de home.html
└── {% block content %} — Contenido adicional: lista de tareas
```

## Archivos relacionados

- [[DAE-Sesion1]] — Resumen del proyecto
- [[Sesion1-Views-Core]] — Vistas de core
- [[Sesion1-Configuracion]] — settings.py (STATIC_URL, TEMPLATES)
