# ENTREGABLE — Sesión 3

## Repositorio

[Link del repositorio de GitHub](https://github.com/<usuario>/<repo>)

---

## Conclusiones

### Modelos implementados

Se implementaron tres modelos (`Exam`, `Question`, `Choice`) con sus respectivas clases `Meta` para personalizar nombres, ordenamiento y comportamiento:

- **Exam**: contiene `title` (CharField 200), `description` (TextField opcional) y `created_at` (DateTimeField con auto_now_add). No tiene relaciones con otros modelos.
- **Question**: tiene un ForeignKey hacia `Exam` con `on_delete=CASCADE` y `related_name="questions"`, un TextField para el texto de la pregunta y un `score` (PositiveIntegerField por defecto 1). Al eliminar un examen, se eliminan todas sus preguntas en cascada.
- **Choice**: tiene un ForeignKey hacia `Question` con `on_delete=CASCADE` y `related_name="choices"`, un CharField(500) para la opción y un BooleanField `is_correct` por defecto False. Al eliminar una pregunta, se eliminan todas sus opciones en cascada.

Las relaciones FK con CASCADE garantizan integridad referencial: no existen preguntas huérfanas sin examen ni opciones huérfanas sin pregunta. `related_name` permite consultas inversas como `exam.questions.all()` y `question.choices.all()`, usadas directamente en los templates.

### Migraciones versionadas

Django generó automáticamente dos migraciones:

1. **0001_initial.py**: Creó las tres tabas de la base de datos (Exam, Question, Choice) con todos sus campos, claves foráneas, índices implícitos por Django (pk_id en FK) y las opciones Meta como comentarios. Django generó automáticamente el campo `id` (BigAutoField) en cada modelo y los campos de audit `created_at` con auto_now_add.
2. **0002_question_score.py**: Se creó manualmente tras agregar el campo `score` al modelo Question. Es un AddField simple con default=1, sin datos previos que requieran un valor por defecto en la migración porque Django lo manejó automáticamente.

### Bug corregido: instance.delete() sobre instancias no guardadas

Al validar que exactamente una opción sea correcta (`correct_count != 1`), el código original intentaba borrar las instancias del formset con `instance.delete()`. Esto fallaba porque `choice_formset.save(commit=False)` devuelve instancias que aún no tienen primary key — no se han guardado en la base de datos. Al llamar `.delete()` sobre ellas, Django intentaba acceder a `.pk` que era None, generando `AttributeError`.

La solución fue eliminar el bucle de `delete()` y en su lugar usar `question_form.add_error(None, '...')` para mostrar el error en el formulario y re-renderizar con status 200, sin tocar la base de datos.

### Casos de validación probados

Se probaron tres escenarios al enviar un POST al view `question_add` con un formset de 4 opciones:

1. **0 opciones correctas** — Status code **200**. La vista re-renderiza el formulario con el mensaje de error en `non_field_errors`. La pregunta no se guarda (count = 0 en Question).
2. **2 opciones correctas** — Status code **200**. Mismo comportamiento: error en el form, no hay guardado.
3. **1 opción correcta** — Status code **302** (redirect a `/exam/<pk>/`). La pregunta se guarda con la relación `exam` y las 4 opciones se guardan con sus respectivas FK hacia la pregunta creada.

Los casos de error devuelven 200 (no 400 explícitamente) porque la vista usa `render()` de Django que por defecto retorna status 200. El redirect 302 confirma que la operación exitosa fluye correctamente a la página de detalle del examen.
