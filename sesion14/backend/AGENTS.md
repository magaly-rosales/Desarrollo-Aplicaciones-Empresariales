# AGENTS.md — contrato del agente de este repositorio

Este archivo lo lee el agente de IA (TecsupCode u otro) al empezar. Es la frontera de confianza de la tienda aplicada a tu
propio asistente: **el agente propone y escribe; las pruebas, la compuerta y las personas deciden.**

## Qué puedes hacer

- Editar **solo** `shop/cart_team.py` (el carrito del equipo) y, en la parte 5, `shop/cart_ai.py` (el de la IA).
- Correr las pruebas por archivo (`python manage.py test shop.tests.test_lines`) cuantas veces haga falta.
- Correr la compuerta sin pantalla: `python manage.py gate --json` (o `--modo ai` cuando arreglas el carrito de la IA).
  Lee el JSON: `verdict`, `tests.failing` y `carts[].result`.
- Correr la auditoría: `python manage.py audit_cart carts/*.json --replay --json --catalogo-fijo`.
- Proponer cambios **en un método por turno** y explicar en dos frases qué cambiaste y por qué.
- Dejar una bitácora corta de cada turno: método tocado, pruebas y veredicto de la compuerta antes y después.

## Qué NO puedes hacer

- Tocar las pruebas (`shop/tests/`), `shop/domain.py` (las reglas), `shop/audit.py`, `shop/gate.py`, `carts/`,
  `shop/seed_data.py`, `config/` ni `requirements.txt`.
- Instalar paquetes ni cambiar versiones.
- Subir al repositorio (`git push`) ni borrar archivos.
- **Leer el precio de la petición.** El precio lo decide el catálogo; si un cambio necesita el precio del cliente para
  que una prueba pase, **detente y pregunta**: la prueba tiene razón.
- **Usar `float` para el dinero.** Todo es `Decimal` con el helper `money` de `shop/domain.py`.
- **Ejecutar `seed_shop`, `migrate` o un pago contra la base** (con `runserver` o la API) sin que la persona lo pida en ese
  turno: borran o cambian datos.
- Dar por terminado nada con la compuerta en rojo. **Terminado = `gate` con código de salida 0.** Si no lo logras, dilo y
  pega la salida de `python manage.py gate`.

## Cómo trabajar

1. Lee solo el método que te piden, su comentario `TODO` y el archivo de pruebas que lo comprueba.
2. Escribe el cambio, corre ese archivo de pruebas y pega la salida.
3. Al terminar el turno corre `python manage.py gate --json` y copia `verdict` y `tests.failed`.
4. Un error del carrito es una excepción de `shop/domain.py` (`CartError` y sus hijas): nunca un `print` ni un valor
   silencioso.

## Las cuatro preguntas de la revisión del diff

Antes de aceptar lo que escribió el agente, la persona responde por escrito, con la línea que lo demuestra:

1. ¿Todo el dinero es **`Decimal`** de principio a fin, con el redondeo hacia arriba en la mitad?
2. ¿El **servidor es la única fuente del precio**? Ninguna línea lee `price` o `unit_price` de la petición.
3. ¿Cada regla de **cantidad y existencias** se cumple con cualquier secuencia de acciones (dos `add` seguidos, quitar de
   más, pagar cuando otro ya compró)?
4. ¿Repetir una acción (doble clic, reintento de red) da **el mismo resultado** que hacerla una vez, por ejemplo el cupón?

Una respuesta «no sé» cuenta como «no»: se vuelve a leer el diff o se corre una prueba que lo demuestre. **La compuerta en
verde no reemplaza estas preguntas**: comprueba lo que las pruebas saben preguntar, no lo que nadie escribió.
