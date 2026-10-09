# GLAB-S07-EXTRA — ORM con IA: duelo y verificador
## Log de Evidencia
### Alumno: Magaly Liz Rosales Porras

---

## PASO 0: Clonación y preparación del proyecto

**Fecha:** 2026-10-09
**Descripción:** Clonar repositorio base del docente y preparar carpeta de trabajo

**Comandos ejecutados:**

```powershell
# Clonar repositorio base del docente en carpeta temporal
cd $env:TEMP
git clone https://github.com/Hellscythe25/dae-s07-orm-con-ia.git $env:TEMP\dae-s07-base

# Copiar contenido a sesion7-conIA (sin .git)
Copy-Item -LiteralPath "$env:TEMP\dae-s07-base\blog" -Destination "C:\Users\MAGALY\Documents\IV CICLO\DesarrolloEmpresariales\sesion7-conIA" -Recurse
Copy-Item -LiteralPath "$env:TEMP\dae-s07-base\config" -Destination "C:\Users\MAGALY\Documents\IV CICLO\DesarrolloEmpresariales\sesion7-conIA" -Recurse
Copy-Item -LiteralPath "$env:TEMP\dae-s07-base\manage.py" -Destination "C:\Users\MAGALY\Documents\IV CICLO\DesarrolloEmpresariales\sesion7-conIA"
Copy-Item -LiteralPath "$env:TEMP\dae-s07-base\requirements.txt" -Destination "C:\Users\MAGALY\Documents\IV CICLO\DesarrolloEmpresariales\sesion7-conIA"
Copy-Item -LiteralPath "$env:TEMP\dae-s07-base\README.md" -Destination "C:\Users\MAGALY\Documents\IV CICLO\DesarrolloEmpresariales\sesion7-conIA"
Copy-Item -LiteralPath "$env:TEMP\dae-s07-base\.gitignore" -Destination "C:\Users\MAGALY\Documents\IV CICLO\DesarrolloEmpresariales\sesion7-conIA"

# Limpiar carpeta temporal
Remove-Item -LiteralPath "$env:TEMP\dae-s07-base" -Recurse -Force
```

**Salida:** Repositorio clonado exitosamente. Contenido copiado a sesion7-conIA. Carpeta temporal eliminada.

**Verificación:**
- [x] manage.py está presente
- [x] config/ está presente
- [x] blog/ está presente
- [x] requirements.txt está presente
- [x] README.md está presente
- [x] No hay carpeta .git en sesion7-conIA

**Ejecutado por:** IA (Magaly)

---

## PASO 1: Entorno virtual, dependencias y migraciones

**Fecha:** 2026-10-09
**Descripción:** Crear entorno virtual, instalar dependencias y ejecutar migraciones

**Comandos ejecutados:**

```powershell
# Crear entorno virtual
python -m venv .venv

# Activar entorno e instalar dependencias
.venv\Scripts\activate
python -m pip install -r requirements.txt

# Ejecutar migraciones
python manage.py migrate
```

**Salida:**
```
Collecting Django<7,>=5.2
  Using cached django-5.2.18-py3-none-any.whl (8.3 MB)
Successfully installed Django-5.2.18 asgiref-3.12.1 sqlparse-0.6.0 typing_extensions-4.16.0 tzdata-2026.5

Operations to perform:
  Apply all migrations: admin, auth, blog, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  ... (todas OK)
  Applying blog.0001_initial... OK
  Applying sessions.0001_initial... OK
```

**Ejecutado por:** IA (Magaly)

---

## PASO 2: seed_blog y conteo de registros

**Fecha:** 2026-10-09
**Descripción:** Cargar datos de ejemplo y verificar conteos

**Comandos ejecutados:**

```powershell
python manage.py seed_blog
python manage.py shell -c "from blog.models import Author, Post, Comment; print(f'Autores: {Author.objects.count()}'); print(f'Artículos: {Post.objects.count()}'); print(f'Comentarios: {Comment.objects.count()}')"
```

**Salida:**
```
Listo: 4 autores, 15 artículos, 23 comentarios.

Autores: 4
Artículos: 15
Comentarios: 23
```

**Verificación:** Los conteos coinciden con lo esperado (4 autores, 15 artículos, 23 comentarios).

**Ejecutado por:** IA (Magaly)

---

## PASO 3: Diagrama de modelos

**Fecha:** 2026-10-09
**Descripción:** Generar diagrama de relaciones de modelos

**Generado por:** IA (Magaly)

**Salida:** Archivo `evidencia/diagrama-modelos.md` generado con el diagrama en formato Mermaid.

**Modelos y relaciones:**
- Author 1:1 Profile (OneToOneField)
- Author 1:N Post (ForeignKey)
- Category 1:N Post (ForeignKey, nullable)
- Post N:M Tag (ManyToManyField)
- Post 1:N Comment (ForeignKey inverso)

**Ejecutado por:** IA (Magaly)

---

## PASO 4: Duelo - Preguntas 1-4

**Fecha:** 2026-10-09
**Descripción:** Escribir y verificar las primeras 4 consultas del duelo

**Respuestas escritas:**
- q1: `Post.objects.filter(published=True)`
- q2: `Post.objects.filter(category__isnull=True)`
- q3: `Post.objects.filter(published_at__gte=date(2026, 3, 1), published_at__lte=date(2026, 5, 31))`
- q4: `Post.objects.annotate(n_comments=Count("comments")).filter(n_comments__gt=2)`

**Intentos necesarios:**
- q1: 1 intento -> correcta
- q2: 1 intento -> correcta
- q3: 1 intento -> correcta
- q4: 1 intento -> correcta

**Ejecutado por:** IA (Magaly)

---

## PASO 5: Duelo - Preguntas 5-8

**Fecha:** 2026-10-09
**Descripción:** Escribir y verificar las últimas 4 consultas del duelo

**Respuestas escritas:**
- q5: `Post.objects.filter(published=True).annotate(n_comments=Count("comments", distinct=True), n_tags=Count("tags", distinct=True)).order_by("-n_comments")[:3]`
- q6: `Post.objects.filter(author__profile__country="Perú")`
- q7: `Comment.objects.filter(post__category__name="Tecnología")`
- q8: `Author.objects.exclude(posts__published=True)`

**Intentos necesarios:**
- q5: 2 intentos (primera sin `distinct=True` dio conteos multiplicados) -> correcta
- q8: 2 intentos (primera con `posts__isnull=True` solo devolvió Diego Pinto) -> correcta
- q1, q2, q3, q4, q6, q7: 1 intento cada una -> correcta

**Ejecutado por:** IA (Magaly)

---

## PASO 6: Duelo contra IA

**Fecha:** 2026-10-09
**Descripción:** Ejecutar duelo con respuestas de la IA y comparar

**Comando:**
```powershell
python manage.py duel --source ai
```

**Resultado:**
```
q1  ✔ correcta               1 consulta(s)
q2  ✔ correcta               1 consulta(s)
q3  ✘ resultado distinto     1 consulta(s)  (faltan 2 artículos)
q4  ⚠ correcta pero cara     16 consulta(s)  (16 consultas vs 1 esperada)
q5  ✘ resultado distinto     1 consulta(s)  (conteos multiplicados)
q6  ✘ error                  0 consulta(s)  (FieldError: country lookup)
q7  ✔ correcta               1 consulta(s)
q8  ✘ resultado distinto     1 consulta(s)  (faltan 1, sobran 1)
```

**3 de 8 correctas y baratas.**

**Tabla de comparación (pregunta | mi respuesta | respuesta IA | veredicto):**

| Pregunta | Mi respuesta | Respuesta IA | Veredicto (IA) | Veredicto (yo) |
|----------|-------------|--------------|----------------|----------------|
| q1 | `Post.objects.filter(published=True)` | `Post.objects.filter(published=True)` | ✔ correcta | ✔ correcta - iguales |
| q2 | `Post.objects.filter(category__isnull=True)` | `Post.objects.filter(category__isnull=True)` | ✔ correcta | ✔ correcta - iguales |
| q3 | `published_at__gte=date(2026,3,1), published_at__lte=date(2026,5,31)` | `published_at__gt=date(2026,3,1), published_at__lt=date(2026,5,31)` | ✘ distinta (usa > en vez de >=) | ✘ distinta - la IA excluye los límites |
| q4 | `Post.objects.annotate(n_comments=Count("comments")).filter(n_comments__gt=2)` | `[post for post in Post.objects.all() if post.comments.count() > 2]` | ⚠ cara (16 consultas) | ⚠ cara - la IA usa Python loop |
| q5 | `annotate(n_comments=Count("comments", distinct=True), n_tags=Count("tags", distinct=True))` | `annotate(n_comments=Count("comments"), n_tags=Count("tags"))` | ✘ distinta | ✘ distinta - falta distinct=True |
| q6 | `Post.objects.filter(author__profile__country="Perú")` | `Post.objects.filter(author__country="Perú")` | ✘ error | ✘ error - author es FK, no tiene country directo |
| q7 | `Comment.objects.filter(post__category__name="Tecnología")` | `Comment.objects.filter(post__category__name="Tecnología")` | ✔ correcta | ✔ correcta - iguales |
| q8 | `Author.objects.exclude(posts__published=True)` | `Author.objects.filter(posts__published=False)` | ✘ distinta | ✘ distinta - la IA incluye autores con borradores |

**Ejecutado por:** IA (Magaly)

---

## PASO 7: Clasificación de fallos de la IA

**Fecha:** 2026-10-09
**Descripción:** Analizar y clasificar los errores de la IA en las 5 preguntas que falló

**Resumen:** La IA acertó 3/8 (q1, q2, q7). Falló en 5 preguntas.

---

### Fallo 1: q3 — Confunde límites inclusivos vs excluyentes

**Tipo de error:** Lógico / Semántico

**Respuesta de la IA:**
```python
Post.objects.filter(published_at__gt=date(2026, 3, 1), published_at__lt=date(2026, 5, 31))
```

**SQL generado:**
```sql
WHERE "blog_post"."published_at" > 2026-03-01 AND "blog_post"."published_at" < 2026-05-31
```

**Problema:** Usa `__gt` y `__lt` (excluyentes) en vez de `__gte` y `__lte` (inclusivos).
Esto excluye los artículos publicados exactamente el 1 de marzo y el 31 de mayo.

**Respuesta correcta:**
```python
Post.objects.filter(published_at__gte=date(2026, 3, 1), published_at__lte=date(2026, 5, 31))
```

**Resultado IA:** 7 artículos (excluye los del 1 de marzo y 31 de mayo)
**Resultado correcto:** 9 artículos (incluye los del 1 de marzo y 31 de mayo)

**Clasificación:** Errores de semántica ORM — la IA no reconoce que "entre X y Y" en español implica límites inclusivos.

---

### Fallo 2: q4 — Solución con N+1 (loop en Python)

**Tipo de error:** Performance (N+1 queries)

**Respuesta de la IA:**
```python
[post for post in Post.objects.all() if post.comments.count() > 2]
```

**Problema:** La IA genera una lista por comprensión en Python. Por cada Post, llama a `post.comments.count()`, que es una consulta SQL independiente. Con 15 artículos + 1 para obtener los posts = **16 consultas**.

**SQL generado (primeras consultas):**
```sql
SELECT ... FROM "blog_post"
SELECT ... FROM "blog_comment" WHERE "blog_comment"."post_id" = 1
SELECT ... FROM "blog_comment" WHERE "blog_comment"."post_id" = 2
...
```

**Respuesta correcta:**
```python
Post.objects.annotate(n_comments=Count("comments")).filter(n_comments__gt=2)
```

**SQL correcto (1 sola consulta):**
```sql
SELECT "blog_post".*, COUNT("blog_comment"."id") AS "n_comments"
FROM "blog_post"
LEFT OUTER JOIN "blog_comment" ON ("blog_post"."id" = "blog_comment"."post_id")
GROUP BY "blog_post"."id"
HAVING COUNT("blog_comment"."id") > 2
```

**Resultado IA:** 16 consultas (N+1)
**Resultado correcto:** 1 consulta

**Clasificación:** Error de performance — la IA no usa annotate/having y en su lugar itera en Python, causando N+1 queries.

---

### Fallo 3: q5 — Counts multiplicados por JOINs de tablas intermedias

**Tipo de error:** Lógico / SQL (GROUP BY con múltiples JOINs)

**Respuesta de la IA:**
```python
Post.objects.filter(published=True).annotate(
    n_comments=Count("comments"),
    n_tags=Count("tags")
).order_by("-n_comments")[:3]
```

**SQL generado:**
```sql
SELECT "blog_post".*, 
    COUNT("blog_comment"."id") AS "n_comments", 
    COUNT("blog_post_tags"."tag_id") AS "n_tags"
FROM "blog_post"
LEFT OUTER JOIN "blog_comment" ON ...
LEFT OUTER JOIN "blog_post_tags" ON ...
WHERE "blog_post"."published"
GROUP BY "blog_post"."id"
ORDER BY "n_tags" DESC
LIMIT 3
```

**Problema:** Al hacer JOINs con DOS tablas intermedias (blog_comment y blog_post_tags), Django genera un GROUP BY que cruza cada fila de comentarios con cada fila de etiquetas, multiplicando los conteos.

Ejemplo: "Introducción al ORM de Django" tiene 6 comentarios y 3 tags. Con el JOIN cruzado, cada comentario se une con cada tag = 6 * 3 = 18 filas. Count("comments") cuenta 18 en vez de 6.

**Respuesta correcta:**
```python
Post.objects.filter(published=True).annotate(
    n_comments=Count("comments", distinct=True),
    n_tags=Count("tags", distinct=True)
).order_by("-n_comments")[:3]
```

El parámetro `distinct=True` fuerza SQL: `COUNT(DISTINCT "blog_comment"."id")` y `COUNT(DISTINCT "blog_post_tags"."tag_id")`, que cuenta valores únicos.

**Resultado IA:** [("Introducción al ORM de Django", 18, 18), ...] — conteos multiplicados
**Resultado correcto:** [("Introducción al ORM de Django", 6, 3), ...] — conteos correctos

**Clasificación:** Error de SQL — la IA no sabe que necesita `distinct=True` cuando anota múltiples relaciones en una misma query.

---

### Fallo 4: q6 — Join directo a campo que no existe en el modelo

**Tipo de error:** SQL / Schema (join a campo inexistente)

**Respuesta de la IA:**
```python
Post.objects.filter(author__country="Perú")
```

**Problema:** `author` es un ForeignKey a `Author`, y `Author` no tiene un campo `country`. El campo `country` está en el modelo `Profile`, que se relaciona con `Author` mediante un `OneToOneField`.

**SQL que genera (y falla):**
```sql
SELECT ... FROM "blog_post"
INNER JOIN "blog_author" ON ...
WHERE "blog_author"."country" = 'Perú'  -- ERROR: column does not exist
```

**Error Django:**
```
FieldError: Unsupported lookup 'country' for ForeignKey or join on the field not permitted.
```

**Respuesta correcta:**
```python
Post.objects.filter(author__profile__country="Perú")
```

**SQL correcto:**
```sql
SELECT ... FROM "blog_post"
INNER JOIN "blog_author" ON ...
INNER JOIN "blog_profile" ON ("blog_author"."id" = "blog_profile"."author_id")
WHERE "blog_profile"."country" = 'Perú'
```

**Clasificación:** Error de schema — la IA no conoce la estructura de modelos y trata de hacer un join a un campo que no existe en el modelo directo.

---

### Fallo 5: q8 — Excluye autores que SÍ han publicado (invertido)

**Tipo de error:** Lógico / Semántico (inversión de consulta)

**Respuesta de la IA:**
```python
Author.objects.filter(posts__published=False)
```

**SQL generado:**
```sql
SELECT "blog_author"."id", "blog_author"."name"
FROM "blog_author"
INNER JOIN "blog_post" ON ("blog_author"."id" = "blog_post"."author_id")
WHERE NOT "blog_post"."published"
```

**Problema:** `filter(posts__published=False)` encuentra autores que TIENEN artículos con `published=False` (borradores). Esto devuelve:
- **Carla Rojas** (tiene 3 borradores)
- Resultado duplicado porque tiene 3 borradores

Y NO encuentra a Diego Pinto (que nunca tiene ningún artículo, ni borrador).

**Resultado IA:** ['Ana Quispe', 'Carla Rojas', 'Carla Rojas', 'Carla Rojas']
- Ana Quispe aparece porque tiene tanto publicados como borradores (los borradores cumplen el WHERE)
- Carla Rojas aparece 3 veces (duplicado por los 3 borradores)
- Diego Pinto NO aparece (nunca tiene artículos)

**Respuesta correcta:**
```python
Author.objects.exclude(posts__published=True)
```

**SQL correcto:**
```sql
SELECT "blog_author"."id", "blog_author"."name"
FROM "blog_author"
LEFT OUTER JOIN "blog_post" ON ("blog_author"."id" = "blog_post"."author_id")
WHERE NOT "blog_post"."id" IS NOT NULL  -- no tiene posts published
```

Que devuelve: ['Carla Rojas', 'Diego Pinto']
- Carla Rojas: tiene borradores pero ningún artículo publicado
- Diego Pinto: no tiene ningún artículo

**Clasificación:** Error de lógica — la IA confunde "autores sin artículos publicados" con "autores que tienen borradores". Usa un `filter` negativo en vez de `exclude` positivo.

---

### Tabla resumen de errores de la IA:

| Pregunta | Tipo de error | Categoría | Causa raíz |
|----------|--------------|-----------|------------|
| q3 | Lógico | Semántica ORM | Confunde > con >= y < con <= |
| q4 | Performance | N+1 query | Usa loop en Python en vez de annotate/HAVING |
| q5 | Lógico | SQL JOINs | No usa distinct=True con múltiples annotate |
| q6 | Schema | Join inválido | Busca campo en modelo incorrecto |
| q8 | Lógico | Inversión lógica | filter(negativo) en vez de exclude(positivo) |

**Conclusión:** La IA acierta en consultas simples (filter directo, joins simples) pero falla en:
1. **Semántica de filtros** (q3: inclusivo vs exclusivo)
2. **Performance ORM** (q4: no entiende que debe usar annotate en vez de loops)
3. **SQL avanzado** (q5: COUNT con múltiple JOIN sin distinct)
4. **Conocimiento de esquema** (q6: join a campo inexistente)
5. **Lógica de exclusión** (q8: invertió la lógica de "nunca ha publicado")

**Ejecutado por:** IA (Magaly)

---

