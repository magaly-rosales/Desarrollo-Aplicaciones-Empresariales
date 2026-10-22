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
