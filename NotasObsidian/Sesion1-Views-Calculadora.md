---
tags:
  - django
  - vistas
  - calculadora
related:
  - DAE-Sesion1
created: 2026-08-28
---

# Sesion1 - Views Calculadora (app calculadora)

## Ruta

`Sesion1/calculadora/views.py`

## Características

- **Stateless**: No interactúa con base de datos
- **Modelos**: No tiene modelos (`models.py` vacío)
- **Templates**: No tiene templates — retorna texto plano con `HttpResponse`
- **Pureza**: Cada vista es una función pura que recibe parámetros y retorna resultado

## Vista: sumar

```python
from django.http import HttpResponse

def sumar(request, a, b):
    resultado = a + b
    return HttpResponse(f'La suma de {a} + {b} = {resultado}')
```

- **URL**: `/app/sumar/<int:a>/<int:b>/`
- **Parámetros**: `a` (int), `b` (int) — extraídos por el URL router
- **Operación**: `a + b`
- **Respuesta**: Plain text → `"La suma de {a} + {b} = {resultado}"`
- **Ejemplo**: `/app/sumar/3/5/` → `"La suma de 3 + 5 = 8"`

## Vista: restar

```python
from django.http import HttpResponse

def restar(request, a, b):
    resultado = a - b
    return HttpResponse(f'La resta de {a} - {b} = {resultado}')
```

- **URL**: `/app/restar/<int:a>/<int:b>/`
- **Parámetros**: `a` (int), `b` (int)
- **Operación**: `a - b`
- **Respuesta**: Plain text → `"La resta de {a} - {b} = {resultado}"`
- **Ejemplo**: `/app/restar/10/4/` → `"La resta de 10 - 4 = 6"`

## Vista: multiplicar

```python
from django.http import HttpResponse

def multiplicar(request, a, b):
    resultado = a * b
    return HttpResponse(f'La multiplicacion de {a} x {b} = {resultado}')
```

- **URL**: `/app/multiplicar/<int:a>/<int:b>/`
- **Parámetros**: `a` (int), `b` (int)
- **Operación**: `a * b`
- **Respuesta**: Plain text → `"La multiplicacion de {a} x {b} = {resultado}"`
- **Ejemplo**: `/app/multiplicar/6/7/` → `"La multiplicacion de 6 x 7 = 42"`

## Archivos relacionados

- [[DAE-Sesion1]] — Resumen del proyecto
- [[Sesion1-URLs-Routing]] — Router
- [[Sesion1-Views-Core]] — Vistas de core
