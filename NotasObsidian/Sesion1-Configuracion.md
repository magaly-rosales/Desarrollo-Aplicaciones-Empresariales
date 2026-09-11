---
tags:
  - django
  - settings
  - configuracion
related:
  - DAE-Sesion1
created: 2026-08-28
---

# Sesion1 - Configuración (settings.py)

## Ruta

`Sesion1/Sesion1/settings.py`

## Configuración principal

### Project name

- **Nombre**: `Sesion1`
- **Versión Django**: 5.2.17

### Debug

- `DEBUG = True` → Modo desarrollo
- `ALLOWED_HOSTS = []` → Sin hosts configurados (no desplegable en producción)

### Secret Key

- `SECRET_KEY` hardcodeado en settings.py (solo para desarrollo)

## Installed Apps

| App | Tipo | Propósito |
|-----|------|-----------|
| `django.contrib.admin` | Django core | Panel de administración |
| `django.contrib.auth` | Django core | Autenticación |
| `django.contrib.contenttypes` | Django core | Content types framework |
| `django.contrib.sessions` | Django core | Sesiones |
| `django.contrib.messages` | Django core | Messaging framework |
| `django.contrib.staticfiles` | Django core | Gestión de archivos estáticos |
| `core` | Custom | Página de inicio y tareas |
| `calculadora` | Custom | Calculadora web |

## URL Configuration

- `ROOT_URLCONF = 'Sesion1.urls'`
- Router raíz en `Sesion1/Sesion1/urls.py`
- Dispatch a sub-apps:
  - `admin/` → Django admin
  - `''` → `core.urls`
  - `'app/'` → `calculadora.urls`

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
- Archivo: `db.sqlite3` en raíz de Sesion1/

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

## Internationalization

- `LANGUAGE_CODE = 'en-us'`
- `TIME_ZONE = 'UTC'`
- `USE_I18N = True`
- `USE_TZ = True`

## Static Files

- `STATIC_URL = 'static/'`
- Gestión por `django.contrib.staticfiles`
- Archivos CSS en: `core/static/core/css/styles.css`

## Archivos relacionados

- [[DAE-Sesion1]] — Resumen del proyecto
- [[Sesion1-URLs-Routing]] — Router y urls.py
- [[Sesion1-Estructura-Archivos]] — Mapa de archivos
