# El carrito revisado por pruebas

Repositorio del laboratorio **extra de la semana 13** de Desarrollo de Aplicaciones Empresariales (DAE).
Una tienda mínima con Django: el **carrito de compras** (agregar, quitar, totales, cupones, existencias y
pago) escrito como lógica pura, una API pequeña encima y un comando para **auditar** un carrito que otra
persona (o una IA) produjo. Los equipos completan el carrito hasta que las pruebas pasan y después revisan
un carrito «escrito por una IA» que compila, responde y tiene fallos sembrados.

La guía del laboratorio (con su rúbrica) está en el campus virtual; aquí está el código.

## Puesta en marcha

```bash
python -m venv .venv
.venv\Scripts\activate          # en Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_shop      # carga el catálogo fijo: 8 productos
python manage.py test           # al principio: casi todo en rojo, a propósito
```

`seed_shop` se puede repetir: borra el catálogo y lo deja **siempre igual**. Con datos fijos se sabe de
antemano cuál es la respuesta correcta de cada prueba.

## Las reglas de la tienda

| Regla | Detalle |
|---|---|
| Dinero | Siempre `Decimal`, nunca `float`. Redondeo al céntimo **hacia arriba en la mitad** (0,005 pasa a 0,01). |
| Precio | Lo decide el catálogo. Una petición **nunca** trae el precio. |
| Cantidad | Entero de 1 en adelante. Quitar más de lo que hay deja la línea en cero y la borra: jamás una cantidad negativa. |
| Existencias | Lo que ya hay en el carrito **más** lo que se agrega no puede pasar de las existencias. Al pagar se vuelve a comprobar. Las existencias nunca bajan de cero. |
| Cupón | Uno por carrito. `BIENVENIDA10` = 10 % del subtotal; `MENOS20` = S/ 20, sin pasar del subtotal. Aplicar otro (o el mismo) **reemplaza**: no se acumula. |
| Totales | `subtotal` = suma de precio × cantidad; `descuento` según el cupón; `igv` = 18 % de (subtotal − descuento); `total` = (subtotal − descuento) + igv, cada parte redondeada. |

El detalle técnico está en `shop/domain.py` (no lo cambies) y en los comentarios `TODO` de `shop/cart_team.py`.

## Parte 1 a 4 — Tu carrito

Completa los `TODO` de `shop/cart_team.py` y corre las pruebas por archivo:

```bash
python manage.py test shop.tests.test_lines      # líneas: agregar y quitar
python manage.py test shop.tests.test_stock      # existencias y pago
python manage.py test shop.tests.test_totals     # dinero y redondeo
python manage.py test shop.tests.test_coupons    # cupones
python manage.py test shop.tests.test_api        # la API (necesita el carrito completo)
python manage.py test                            # todo
```

## Parte 5 — El duelo: tu carrito contra el de la IA

```bash
python manage.py duelo                 # las mismas pruebas contra tu carrito y contra el de la IA
python manage.py duelo --modo ai       # el detalle de lo que falla en el de la IA
```

La versión de la IA está en `shop/cart_ai.py`. Se activa con la variable `SHOP_MODE`; así también se usa en
las pruebas sueltas y en la API:

```bash
# PowerShell
$env:SHOP_MODE = "ai"; python manage.py test; Remove-Item Env:SHOP_MODE
# CMD
set SHOP_MODE=ai && python manage.py test && set SHOP_MODE=
```

No se arregla el archivo de la IA con las pruebas a ciegas: primero se clasifica cada fallo (prueba, mensaje,
causa y si se vería a mano) y luego se corrige uno por uno.

## Parte 6 — Auditar un carrito (sin pantalla)

`carts/` trae seis carritos declarados (JSON) que salieron de la tienda de la IA. El comando los revisa contra el
catálogo y las reglas, sin abrir ninguna pantalla:

```bash
python manage.py audit_cart carts/*.json                 # informe legible
python manage.py audit_cart carts/*.json --json          # informe en JSON, para otro programa o un agente
python manage.py audit_cart carts/*.json --replay        # además, reconstruye cada carrito con la implementación activa
python manage.py audit_cart carts/*.json --strict        # termina con error si algún carrito tiene hallazgos
python manage.py audit_cart carts/*.json --catalogo-fijo # usa el catálogo fijo, sin la base de datos
```

Con `--replay` y `SHOP_MODE=ai` se ve qué calcula el carrito de la IA; con `SHOP_MODE=team`, qué calcula el tuyo.
La API tiene el mismo servicio: `POST /api/cart/audit/` (con `?replay=1`).

Códigos de hallazgo: `PRICE_MISMATCH`, `OVER_STOCK`, `BAD_QTY`, `UNKNOWN_SKU`, `MULTIPLE_COUPONS`, `COUPON_INVALID`,
`TOTAL_MISMATCH`, `REPLAY_MISMATCH`, `REPLAY_REJECTED`, `REPLAY_UNAVAILABLE`.

## Parte 7 — La compuerta: el agente propone, la compuerta decide

Si trabajas con un agente de IA, primero lee **`AGENTS.md`**: qué puede tocar (un método por turno, solo
`shop/cart_team.py` o `shop/cart_ai.py`), qué no (las pruebas, las reglas, el precio de la petición) y las cuatro
preguntas con las que la persona revisa cada diff.

La compuerta junta los dos oráculos sin pantalla —las pruebas y la auditoría con `--replay`— y da un veredicto con
código de salida, para que un agente o un script sepa si su cambio se acepta:

```bash
python manage.py gate                 # juzga tu carrito (SHOP_MODE o team)
python manage.py gate --modo ai       # juzga el carrito de la IA
python manage.py gate --json          # el mismo veredicto en JSON: verdict, tests.failing, carts[].result
```

| Código | Veredicto | Cuándo |
|---|---|---|
| 0 | `aceptar` | Todas las pruebas pasan y cada carrito de `carts/` da lo esperado |
| 1 | `rechazar` | Alguna prueba falla o algún carrito no da lo esperado |
| 2 | `no_disponible` | El modo no existe en esta copia |

«Lo esperado» depende del carrito: un carrito con una cantidad mala, un producto desconocido o más unidades que las
existencias debe ser **rechazado** por la implementación; cualquier otro debe dar los totales de la fórmula de referencia.
La regla está en `shop/gate.py`, en veinte líneas que se pueden leer.

**Terminado = compuerta en 0.** Pero la compuerta solo sabe lo que las pruebas preguntan: las cuatro preguntas de
`AGENTS.md` las responde una persona.

## La API

```bash
python manage.py runserver
```

| Método y ruta | Qué hace | Errores |
|---|---|---|
| `GET /api/cart/` | El carrito de esta sesión, con totales | |
| `POST /api/cart/items/` `{"sku": "MOU-01", "qty": 2}` | Agrega (201) | 404 producto, 409 existencias, 400 cuerpo o cantidad |
| `DELETE /api/cart/items/<sku>/?qty=1` | Quita (sin `qty`, la línea entera) | 404, 400 |
| `POST /api/cart/coupon/` `{"code": "BIENVENIDA10"}` | Aplica el cupón | 400 |
| `POST /api/cart/checkout/` | Paga: baja las existencias y vacía el carrito (201) | 400 vacío, 409 existencias |
| `POST /api/cart/audit/` | Audita un carrito declarado | |

El carrito vive en la **sesión** del servidor. La API no tiene autenticación ni protección CSRF: es un laboratorio
(en una tienda real irían las dos).

## Estructura

| Ruta | Para qué |
|---|---|
| `shop/cart_team.py` | **Tu** carrito (con `TODO`) |
| `shop/cart_ai.py` | El carrito que escribió la IA, tal cual |
| `shop/domain.py` | Reglas, errores y el cálculo de referencia (no se cambia) |
| `shop/impl.py` | Elige qué carrito se usa según `SHOP_MODE` |
| `shop/views.py`, `urls.py`, `catalog.py` | La API (HTTP, sesión y base de datos) |
| `shop/audit.py` y `management/commands/` | La auditoría, `audit_cart`, `duelo`, `gate`, `seed_shop` |
| `shop/gate.py` | La regla de la compuerta: qué se espera de cada carrito y cuándo se acepta un cambio |
| `AGENTS.md` | El contrato del agente y las cuatro preguntas de revisión del diff |
| `shop/tests/` | Las pruebas: el oráculo |
| `carts/` | Carritos declarados para auditar |

## Convenciones del curso

Código, nombres y comentarios en inglés; explicaciones y entregables en español. PEP 8.
