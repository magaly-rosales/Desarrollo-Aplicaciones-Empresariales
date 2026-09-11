---
tags:
  - django
  - settings
  - configuracion
related:
  - Overview-Sesion2
created: 2026-08-28
---

# Sesion2 - Configuración (settings.py)

## Ruta

`Sesion2/Sesion2/settings.py`

## Configuración principal

- **Nombre**: `Sesion2`
- **Versión Django**: 5.2.17
- **DEBUG**: `True`
- **ALLOWED_HOSTS**: `[]` (no desplegable en producción)
- **SECRET_KEY**: hardcodeado en settings.py (solo desarrollo)

## Installed Apps

| App | Tipo | Propósito |
|-----|------|-----------|
| `core` | Custom | Página de inicio y tareas |
| `django.contrib.admin` | Django core | Panel de administración |
| `django.contrib.auth` | Django core | Autenticación |
| `django.contrib.contenttypes` | Django core | Content types framework |
| `django.contrib.sessions` | Django core | Sesiones |
| `django.contrib.messages` | Django core | Messaging framework |
| `django.contrib.staticfiles` | Django core | Gestión de archivos estáticos |

## URL Configuration

- `ROOT_URLCONF = 'Sesion2.urls'`
- Router raíz en `Sesion2/Sesion2/urls.py`
- Dispatch a sub-apps:
  - `admin/` → Django admin
  - `''` → `core.urls`

## Database

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

- Motor: `django.db.backends.sqlite3`
- Archivo: `db.sqlite3` en raíz de Sesion2/

## Template Configuration

```python
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,  # Busca templates dentro de cada app
    ...
}]
```

- `APP_DIRS = True` → Django busca `app/templates/` automáticamente

## Static Files

- `STATIC_URL = 'static/'`
- Gestión por `django.contrib.staticfiles`
- Archivos CSS en: `core/static/core/css/styles.css`

## Archivos relacionados

- [[Overview-Sesion2]] — Resumen del proyecto
- [[Sesion2-URLs-Routing]] — Router y urls.py
- [[Sesion2-Estructura-Archivos]] — Mapa de archivos
