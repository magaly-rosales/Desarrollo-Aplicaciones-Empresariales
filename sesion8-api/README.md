# Laboratorio 8: API REST con Django REST Framework

## Tabla de la API

| Método | Ruta | Qué hace | Éxito | Errores |
|---|---|---|---|---|
| GET | `/api/exams/` | Lista exámenes (de 5 en 5) | 200 | 401 |
| POST | `/api/exams/` | Crea un examen (`title`) | 201 | 400, 401 |
| GET | `/api/exams/{id}/` | Detalle del examen | 200 | 401, 404 |
| PUT / PATCH | `/api/exams/{id}/` | Reemplaza / modifica | 200 | 400, 401, 404 |
| DELETE | `/api/exams/{id}/` | Elimina | 204 | 401, 404 |
| GET | `/api/questions/` | Lista preguntas con sus opciones | 200 | 401 |
| GET | `/api/questions/?exam=ID` | Filtra por examen | 200 | 401 |
| GET | `/api/questions/?search=texto` | Busca en el texto | 200 | 401 |
| GET | `/api/questions/?page=2` | Segunda página | 200 | 401, 404 |
| POST | `/api/questions/` | Crea pregunta con opciones anidadas | 201 | 400, 401 |
| GET | `/api/questions/{id}/` | Detalle | 200 | 401, 404 |
| PUT / PATCH | `/api/questions/{id}/` | Modifica | 200 | 400, 401, 404 |
| DELETE | `/api/questions/{id}/` | Elimina | 204 | 401, 404 |
| GET | `/api/choices/` | Lista opciones (`?search=`) | 200 | 401 |
| POST | `/api/choices/` | Crea opción (necesita `question`) | 201 | 400, 401 |
| GET | `/api/choices/{id}/` | Detalle | 200 | 401, 404 |
| PUT / PATCH | `/api/choices/{id}/` | Modifica | 200 | 400, 401, 404 |
| DELETE | `/api/choices/{id}/` | Elimina | 204 | 401, 404 |