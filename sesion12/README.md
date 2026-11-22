# Laboratorio 12: Servicios Web (React + Axios consumiendo Django)

**Estudiante:** Magaly Liz Rosales Porras


Una aplicación de React consume, con Axios, la API de cuestionarios de Django (laboratorio 8). Lista, crea y elimina exámenes, y resuelve en pantalla los tres estados de una petición: carga, datos y error.

## 1. Estructura

```
sesion12/
├── backend/     API de Django (laboratorio 8) con CORS habilitado
├── frontend/    Proyecto de React (laboratorio 11) con Axios
├── evidencia/   Notas de las pruebas de error
└── README.md
```

## 2. Qué origen espera cada lado

| Lado | Dirección | Qué espera |
|---|---|---|
| Servidor (Django) | `http://localhost:8000` | Acepta peticiones del navegador **solo** desde `http://localhost:5173` y `http://127.0.0.1:5173` (sin comodín) |
| Cliente (React) | `http://localhost:5173` | Encuentra la API en `http://localhost:8000/api` y envía un token en la cabecera `Authorization` |

Si Vite arranca en otro puerto, hay que agregar ese origen a `CORS_ALLOWED_ORIGINS` en `backend/config/settings.py`.

## 3. Cómo levantar el servidor (Django)

Desde la carpeta `backend`:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_quiz
python manage.py runserver
```

`seed_quiz` carga los exámenes de ejemplo y crea los usuarios `profe` y `agente` con su token. **Borra y vuelve a crear los exámenes**, así que se usa solo la primera vez. Para ver el token de `profe` sin tocar los datos:

```bash
python manage.py drf_create_token profe
```

El servidor queda en `http://localhost:8000/api/exams/`.

## 4. Cómo levantar el cliente (React)

Desde la carpeta `frontend`:

```bash
npm install
```

Crea el archivo `.env.local` (no se sube a Git; la plantilla es `.env.example`) con la dirección de la API y el token de `profe`:

```
VITE_API_BASE_URL=http://localhost:8000/api
VITE_API_TOKEN=<token de profe>
```

Luego:

```bash
npm run dev
```

La aplicación queda en `http://localhost:5173`. Django debe estar encendido antes de abrirla.

## 5. Qué hace la aplicación

| Ruta | Pantalla | Petición |
|---|---|---|
| `/` | Listado de exámenes | `GET /api/exams/` al entrar |
| `/` | Botón **Eliminar** | `DELETE /api/exams/{id}/` y vuelve a pedir la lista |
| `/exams/new` | Formulario de alta | `POST /api/exams/` y vuelve al listado |

Todas las peticiones salen de un solo módulo, `frontend/src/api/quizApi.js`, donde está la dirección base. Ningún componente escribe una URL a mano.

## 6. Los tres estados de la pantalla de listado

| Estado | Cuándo | Qué se muestra |
|---|---|---|
| Carga | Mientras llega la respuesta | Cinco barras grises (esqueleto) |
| Datos | La API responde bien | Tabla con ID, título, número de preguntas, fecha y botón **Eliminar** |
| Error | No hay respuesta o la API rechaza la petición | Mensaje específico y botón **Reintentar** |

Los mensajes de error distinguen la causa (`frontend/src/utils/getErrorMessage.js`): servidor apagado o CORS, falta de permiso (401 o 403), recurso inexistente (404), falla del servidor (5xx) y errores de validación (400), donde se muestra el mensaje que devuelve la API.

## 7. CORS

En `backend/config/settings.py`:

- `corsheaders` está en `INSTALLED_APPS`.
- `corsheaders.middleware.CorsMiddleware` va justo después de `SecurityMiddleware`.
- `CORS_ALLOWED_ORIGINS` lista solo los dos orígenes del cliente.

La prueba con un origen no autorizado y el mensaje que muestra el navegador sin CORS están en `evidencia/cors-error.md`.

## 8. Observaciones

- El token vive en `.env.local`, fuera del repositorio. Va dentro del código que descarga el navegador, así que sirve solo para desarrollo. En producción, la identidad se resolvería con un inicio de sesión.
- La API pagina de 5 en 5; el listado muestra la primera página y el total ("2 de 2 exámenes").
- En modo desarrollo, React ejecuta el efecto dos veces y por eso la petición `GET` aparece duplicada en la pestaña Network. No ocurre en producción.
- La clase `AgentPermission` del laboratorio 8 sigue con su `TODO` y deja pasar todo. No afecta a este laboratorio.