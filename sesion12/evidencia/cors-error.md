# Evidencia: error de CORS provocado

## Qué se hizo

1. Se comentaron los dos orígenes de `CORS_ALLOWED_ORIGINS` en `backend/config/settings.py`.
2. Se recargó la app de React (`http://localhost:5173`).
3. Se leyó el mensaje en la consola del navegador.
4. Se restauraron los orígenes.

## Mensaje de la consola

```
Access to XMLHttpRequest at 'http://localhost:8000/api/exams/' from origin
'http://localhost:5173' has been blocked by CORS policy: No
'Access-Control-Allow-Origin' header is present on the requested resource.
```

Además, la petición `GET http://localhost:8000/api/exams/` falla con `net::ERR_FAILED`.

## Qué significa

El navegador bloquea la respuesta de la API porque React (origen `http://localhost:5173`) y Django (origen `http://localhost:8000`) tienen puertos distintos, así que son orígenes distintos. Django debe decir de forma explícita que acepta al de React enviando el encabezado `Access-Control-Allow-Origin`. Sin ese encabezado, el navegador descarta la respuesta, aunque Django la haya generado con normalidad.

## Qué se ve en la interfaz

El estado de error de la página: el mensaje "No se pudo conectar con el servidor. Revisa que Django esté encendido y que CORS permita este origen." y el botón **Reintentar**.

## Cómo se corrige

Autorizar solo el origen de React, sin comodín:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
```

El middleware `corsheaders.middleware.CorsMiddleware` va justo después de `SecurityMiddleware`.

## Comprobación del origen no autorizado

Con `curl`, un origen que no está en la lista no recibe el encabezado:

```
curl -i -H "Origin: http://evil.example" http://localhost:8000/api/exams/
```

La respuesta no incluye `access-control-allow-origin`.