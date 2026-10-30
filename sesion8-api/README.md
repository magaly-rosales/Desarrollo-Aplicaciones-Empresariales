# Laboratorio 8: API REST de cuestionarios con Django REST Framework

**Alumna:** Magaly Liz Rosales Porras
**Institución:** Tecsup, Diseño y Desarrollo de Software, IV ciclo, sección 4-C24-A
**Curso:** Desarrollo de Aplicaciones Empresariales
**Docente:** Michael Montgomery Rosell
**Periodo:** 2026-2
**Laboratorio:** GLAB-S08

API REST sin pantalla (headless) para un sistema de cuestionarios. Expone tres recursos (`exams`, `questions` y `choices`) con Django REST Framework, valida los datos en el servidor y se prueba con Postman, Newman y las pruebas de Django.

## 1. Puesta en marcha

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_quiz
python manage.py runserver
```

`seed_quiz` crea los datos de ejemplo y los usuarios `profe` y `agente`, e imprime sus tokens. Los tokens no se guardan en el repositorio.

Rutas útiles:

- API: `http://127.0.0.1:8000/api/`
- Documentación: `http://127.0.0.1:8000/api/docs/`
- Login del navegador: `http://127.0.0.1:8000/api-auth/login/`

## 2. Configuración de REST_FRAMEWORK

En `config/settings.py`:

- **Autenticación:** Token (para Postman y clientes), Sesión (para la API navegable) y Basic.
- **Permisos:** `IsAuthenticated`; hay que estar identificada para usar la API. Se añade `AgentPermission`, que en este laboratorio deja pasar todo (parte opcional del profesor, no implementada).
- **Paginación:** `PageNumberPagination` con `PAGE_SIZE = 5`.
- **Esquema:** `drf-spectacular` (`/api/schema/` y `/api/docs/`).

## 3. Serializadores y decisión de relación

- `ExamSerializer`: `id`, `title`, `created_at` y `question_count` (solo lectura).
- `QuestionSerializer`: `id`, `exam`, `text`, `choices` y `created_at`. Las opciones viajan **anidadas** dentro de la pregunta y el examen viaja como **id**. Crear o modificar una pregunta se hace dentro de una transacción.
- `ChoiceSerializer`: `id`, `text` e `is_correct`; es el que va anidado dentro de la pregunta.
- `ChoiceDetailSerializer`: se usa en `/api/choices/` e incluye `question` como id.

**Decisión de relación:** las opciones van anidadas porque una opción no tiene sentido sin su pregunta, y así una pregunta completa se crea en una sola petición. El examen va por id para no repetir sus datos en cada pregunta.

## 4. Validación

- Una pregunta necesita al menos **dos opciones**.
- Debe haber **exactamente una opción correcta**.
- Al crear o modificar una opción suelta, no se permite una segunda opción correcta en la misma pregunta.
- Los tipos incorrectos y los campos ausentes los rechaza DRF con código 400.

## 5. ViewSets y router

- `ExamViewSet`, `QuestionViewSet` y `ChoiceViewSet` son `ModelViewSet` (CRUD completo).
- Se registran en un `DefaultRouter` con las rutas `exams`, `questions` y `choices`.
- `QuestionViewSet` usa `select_related` y `prefetch_related` para evitar consultas de más, filtra por `?exam=` y busca por texto con `?search=`.
- `ChoiceViewSet` busca por texto con `?search=`.

## 6. Cinco operaciones (resultados reales)

| Operación | Petición | Código |
|---|---|---|
| Listar | `GET /api/questions/` | 200 |
| Detalle | `GET /api/questions/1/` | 200 |
| Crear | `POST /api/questions/` | 201 |
| Modificar | `PATCH /api/questions/{id}/` | 200 |
| Eliminar | `DELETE /api/questions/{id}/` | 204 |

Lo mismo se repitió con `/api/choices/` (listar 200, crear 201, modificar 200, eliminar 204).

## 7. Errores de validación (mensajes reales)

| Caso | Código | Mensaje de la API |
|---|---|---|
| Campos obligatorios ausentes | 400 | `exam`: "Este campo es requerido." y `choices`: "Este campo es requerido." |
| Tipo incorrecto en `exam` | 400 | "Tipo incorrecto. Se esperaba valor de clave primaria y se recibió str." |
| Sin opción correcta, o con dos | 400 | `choices`: "Debe haber exactamente una opción correcta." |
| Segunda opción correcta en una pregunta (`/api/choices/`) | 400 | "Ya existe una opción correcta para esta pregunta. Al marcar esta como correcta, la anterior dejará de serlo." |
| Página que no existe (`?page=99`) | 404 | "Página inválida." |
| Recurso que no existe | 404 | "No encontrado." |
| Sin token | 401 | Credenciales no proporcionadas |

## 8. Filtro, búsqueda y paginación

- Filtro: `GET /api/questions/?exam=1` devuelve solo las preguntas de ese examen.
- Búsqueda: `GET /api/questions/?search=prefetch` busca en el texto de la pregunta.
- Paginación: de 5 en 5. La respuesta trae `count`, `next`, `previous` y `results`. Con 18 preguntas hay 4 páginas: la página 2 tiene `next` y `previous`, y la página 4 tiene `next` igual a `null`.

## 9. Tabla de la API

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

## 10. Pruebas de Django

```bash
python manage.py test quiz.tests.test_api
```

```
Found 15 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
...............
----------------------------------------------------------------------
Ran 15 tests in 0.476s

OK
Destroying test database for alias 'default'...
```

Las pruebas `test_permissions` y `test_quizctl` no pasan porque son partes opcionales que el profesor dejó con `TODO(team)` y no las implementé.

## 11. Postman y Newman

La colección y el entorno están en `evidencia/postman/` (4 carpetas: operaciones de preguntas, operaciones de opciones, errores y validación, y filtro, búsqueda y paginación).

Resultado de Newman: **21 requests, 37 assertions, 0 fallos**.

Para repetirlo: borrar `db.sqlite3`, correr `migrate` y `seed_quiz`, agregar 10 preguntas de ejemplo (para que existan 4 páginas de 5), prender el servidor y correr:

```bash
newman run evidencia\postman\quiz-api.postman_collection.json -e evidencia\postman\quiz-api.postman_environment.json --env-var "token=<TOKEN>"
```

El token no se guarda en el repositorio; el campo `token` del entorno está vacío a propósito.

## 12. Uso de IA

Usé OpenCode con un modelo local para generar partes del código y los scripts de prueba. Yo revisé los resultados en el navegador y en Postman, y corregí los errores que aparecieron: la barra final de las rutas, el login del navegador, el recurso de opciones y el formato del entorno de Postman.

