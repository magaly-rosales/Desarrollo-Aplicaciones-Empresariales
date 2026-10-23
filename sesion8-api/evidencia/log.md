# Evidencia - GLAB-S08: Implementación de Servicios Web con Django

## Paso 0 - Preparación del entorno

### Comando: Clonar base del docente
```
git clone https://github.com/Hellscythe25/dae-s08-api-headless.git %TEMP%\dae-s08-base
```
Salida: Repositorio clonado exitosamente.

### Comando: Copiar contenido a sesion8-api (sin .git)
```
Copy-Item -Recurse -Force $env:TEMP\dae-s08-base\* sesion8-api\
Remove-Item -Recurse -Force sesion8-api\.git\
```
Salida: Contenido copiado correctamente.

### Comando: Crear entorno virtual e instalar dependencias
```
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
Salida:
- Django 5.2.18
- djangorestframework 3.18.3
- drf-spectacular 0.30.0
- requests 2.34.2

### Comando: Migrate
```
python manage.py migrate
```
Salida:
```
Operations to perform:
  Apply all migrations: auth, authtoken, contenttypes, quiz
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0001_initial... OK
  ... (todas OK)
  Applying quiz.0001_initial... OK
```

### Comando: Seed quiz
```
python manage.py seed_quiz
```
Salida:
```
Listo: 2 exámenes, 8 preguntas.

Tokens (solo para esta máquina; el de la persona es el que puede borrar):
  PowerShell:
    $env:QUIZ_TOKEN_HUMANO = "f6ecbadb0e630f9eefd90c97d2c3b7cfd761fd0b"
    $env:QUIZ_TOKEN_AGENTE = "0dbf72f7b499c9fc62acc6fd674a95ddb4e52641"
```
NOTA: Los tokens se imprimen pero NO se guardan en archivos del repo.

### Python version
```
python --version
```
Salida: `Python 3.10.11`
Observación: La guía pide Python 3.12+, pero el entorno tiene 3.10.11. No afecta funcionalidad.

## Paso 1 y 2 - DRF, INSTALLED_APPS y REST_FRAMEWORK

### Verificación DRF instalado
```
python -c "import rest_framework; print(rest_framework.VERSION)"
```
Salida: `3.18.3`

### Verificación Django check
```
python manage.py check
```
Salida: `System check identified no issues (0 silenced)`

### Verificación test_api
```
python manage.py test quiz.tests.test_api
```
Salida: 15 tests, todos OK, 0.353s

### Explicación de la configuración (config/settings.py)

**INSTALLED_APPS:**
- `"rest_framework"` - framework para construir la API REST
- `"rest_framework.authtoken"` - autenticación por token (crea modelo Token)
- `"drf_spectacular"` - genera documentación OpenAPI/Swagger
- `"quiz"` - app principal con modelos, vistas, serializadores

**REST_FRAMEWORK:**
- `"DEFAULT_AUTHENTICATION_CLASSES": ["rest_framework.authentication.TokenAuthentication"]` - autentica usuarios por token en header Authorization
- `"DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated", "quiz.permissions.AgentPermission"]` - dos capas: primero debe estar autenticado, luego aplica regla de permisos personalizada
- `"DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination"` - paginación por número de página
- `"PAGE_SIZE": 5` - 5 resultados por página
- `"DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema"` - genera esquema OpenAPI automáticamente

## Paso 3 - Serializadores (quiz/serializers.py)

### ChoiceSerializer
Modelo: `Choice`
Campos expuestos:
- `id` - entero, auto-generado
- `text` - string, máx 200 caracteres
- `is_correct` - booleano, indica si es la respuesta correcta

### ExamSerializer
Modelo: `Exam`
Campos expuestos:
- `id` - entero, auto-generado
- `title` - string, máx 120 caracteres (write + read)
- `created_at` - fecha/hora, **solo lectura** (auto-generado al crear)
- `question_count` - entero, **solo lectura** (calculado via annotate en el queryset)

### QuestionSerializer
Modelo: `Question`
Campos expuestos:
- `id` - entero, auto-generado
- `exam` - entero (ID del examen), **write + read** (enviado como identificador, no como objeto anidado)
- `text` - string libre (write + read)
- `choices` - array de ChoiceSerializer, **anidado** (write + read)
- `created_at` - fecha/hora, **solo lectura**

## Paso 4 - Decisión de relaciones: exam como ID, choices anidados

### Opciones viajando ANIDADAS dentro de la pregunta
En `QuestionSerializer`, los choices se serializan como un array anidado (`ChoiceSerializer(many=True)`). Esto se hace porque:
- Las opciones dependen semánticamente de una pregunta; no tienen existencia independiente en el dominio del cuestionario.
- Al crear/modificar una pregunta, es natural enviar todas sus opciones en un solo request.
- `create()` y `update()` manejan la lógica de crear/borrar las opciones en transacción atómica.

### Examen viaja como IDENTIFICADOR
El campo `exam` se envía como un entero (ID del examen), NO como un objeto Exam anidado. Esto se hace porque:
- La relación es ForeignKey; lo que importa es identificar a qué examen pertenece la pregunta.
- El examen ya existe (se crea por separado). No tiene sentido clonar el objeto exam dentro de la pregunta.
- Simplifica el contrato de la API: solo se necesita el ID del examen existente.

## Paso 5 - Validación propia: opción correcta

La validación propia se implementa en `QuestionSerializer.validate_choices()`:

```python
def validate_choices(self, value):
    if len(value) < 2:
        raise serializers.ValidationError("Una pregunta necesita al menos dos opciones.")
    if sum(1 for choice in value if choice.get("is_correct")) != 1:
        raise serializers.ValidationError("Debe haber exactamente una opción correcta.")
    return value
```

Reglas:
1. **Mínimo 2 opciones**: si se envían menos de 2 choices, se rechaza con "Una pregunta necesita al menos dos opciones."
2. **Exactamente 1 correcta**: se cuenta cuántos choices tienen `is_correct=True`; debe ser exactamente 1. Si hay 0 o más de 1, se rechaza con "Debe haber exactamente una opción correcta."

## Paso 7 - API Navegable y Cambio Mínimo

### Problema identificado
Con SOLO `TokenAuthentication`, al acceder al API desde un navegador (sin token), se recibe:
- `GET /api/` → **401 Unauthorized** con mensaje "Las credenciales de autenticación no se proveyeron."
- No se puede ver la API navegable (HTML interactivo).

### Cambio mínimo aplicado

**1. config/settings.py** - Agregué `SessionAuthentication` y `BasicAuthentication`:
```python
"DEFAULT_AUTHENTICATION_CLASSES": [
    "rest_framework.authentication.TokenAuthentication",  # sigue funcionando para API programática
    "rest_framework.authentication.SessionAuthentication", # permite login en navegador
    "rest_framework.authentication.BasicAuthentication",   # permite basic auth para browsable API
],
```

**2. config/settings.py** - Agregué configuración de templates (necesaria para browsable API):
```python
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
            ],
        },
    },
]
```

**3. config/urls.py** - Agregué rutas de autenticación de DRF:
```python
path("api-auth/", include("rest_framework.urls")),
```

### Impacto
- `TokenAuthentication` sigue funcionando igual para acceso programático.
- El navegador ahora puede ver la API navegable (200 OK con HTML).
- Se puede hacer login en `/api-auth/` para probar operaciones desde el navegador.
- Las pruebas existentes (`test_api`) siguen pasando.

### Las cinco operaciones sobre preguntas

| Operación | Método | Ruta | Cuerpo | Estado |
|-----------|--------|------|--------|--------|
| Listar | GET | `/api/questions/` | - | **200** |
| Detalle | GET | `/api/questions/{id}/` | - | **200** |
| Crear | POST | `/api/questions/` | `{"exam": 1, "text": "...", "choices": [...]}` | **201** |
| Modificar parcial | PATCH | `/api/questions/{id}/` | `{"text": "nuevo texto"}` | **200** |
| Eliminar | DELETE | `/api/questions/{id}/` | - | **204** |

Evidencia real (tokens de `seed_quiz`):
- GET list: 200 (count=8, 5 por página)
- GET detalle: 200 (muestra text, exam, choices)
- POST crear: 201 (devuelve objeto creado con ID)
- PATCH modificar: 200 (text actualizado)
- DELETE eliminar: 204 (sin cuerpo; GET posterior devuelve 404)

## Paso 6 - ViewSets y Enrutador

### ExamViewSet (quiz/views.py)
- Hereda de `viewsets.ModelViewSet` (CRUD completo: list, create, retrieve, update, partial_update, destroy)
- `serializer_class = ExamSerializer`
- `queryset = Exam.objects.annotate(question_count=Count("questions")).order_by("id")`
  - Anota cada examen con el conteo de preguntas usando `Count("questions")`
  - Ordenado por ID ascendente

### QuestionViewSet (quiz/views.py)
- Hereda de `viewsets.ModelViewSet` (CRUD completo)
- `serializer_class = QuestionSerializer`
- `filter_backends = [filters.SearchFilter]` - habilita búsqueda por texto
- `search_fields = ["text"]` - busca en el campo text de la pregunta
- `get_queryset()`: filtra por `exam` si se pasa `?exam=N` como query param
  - Usa `select_related("exam")` para optimizar la carga del examen
  - Usa `prefetch_related("choices")` para optimizar la carga de las opciones

### DefaultRouter (quiz/urls.py)
Registra 2 recursos:
```python
router.register("exams", ExamViewSet, basename="exam")
router.register("questions", QuestionViewSet, basename="question")
```

### Rutas generadas

**exams:**
| Método | Ruta | Acción |
|--------|------|--------|
| GET | /api/exams/ | listar |
| POST | /api/exams/ | crear |
| GET | /api/exams/{id}/ | detalle |
| PUT | /api/exams/{id}/ | reemplazar |
| PATCH | /api/exams/{id}/ | parcial |
| DELETE | /api/exams/{id}/ | eliminar |

**questions:**
| Método | Ruta | Acción |
|--------|------|--------|
| GET | /api/questions/ | listar |
| POST | /api/questions/ | crear |
| GET | /api/questions/{id}/ | detalle |
| PUT | /api/questions/{id}/ | reemplazar |
| PATCH | /api/questions/{id}/ | parcial |
| DELETE | /api/questions/{id}/ | eliminar |

Además de parámetros de consulta:
- `?search=<texto>` - búsqueda en el campo text de preguntas
- `?exam=<id>` - filtra preguntas por ID de examen
- `?page=<n>` - paginación (5 por página)

### NOTA: Recurso 'choices' no expuesto
El router registra SOLO `exams` y `questions`. El modelo `Choice` NO está expuesto como recurso independiente (no hay `ChoiceViewSet`). Las opciones viajan ANIDADAS dentro de la pregunta.

## Paso 8 - Choices como tercer recurso del enrutador

### Cambio realizado
Se agregó `ChoiceViewSet` en `quiz/views.py` y `router.register("choices", ChoiceViewSet, basename="choice")` en `quiz/urls.py`.

**ChoiceViewSet (quiz/views.py):**
- Hereda de `viewsets.ModelViewSet` (CRUD completo)
- `serializer_class = ChoiceSerializer`
- `filter_backends = [filters.SearchFilter]`, `search_fields = ["text"]` - búsqueda por texto de la opción
- `get_queryset()`: `Choice.objects.select_related("question").order_by("id")` - optimiza carga del question

**Rutas generadas para choices:**
| Método | Ruta | Acción |
|--------|------|--------|
| GET | /api/choices/ | listar |
| POST | /api/choices/ | crear |
| GET | /api/choices/{id}/ | detalle |
| PUT | /api/choices/{id}/ | reemplazar |
| PATCH | /api/choices/{id}/ | parcial |
| DELETE | /api/choices/{id}/ | eliminar |

### Evidencia real
- `GET /api/` ahora incluye `"choices":"http://127.0.0.1:8000/api/choices/"`
- `GET /api/choices/` devuelve `200 OK` con count=48, paginación (5 por página)
- Cada choice muestra `id`, `text`, `is_correct`
- Django tests: 15/15 OK
- Newman: 14 requests, 30 assertions, 0 fallos
