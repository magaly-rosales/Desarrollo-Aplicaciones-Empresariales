"""HTTP layer: JSON in, JSON out. All the shop rules live in the cart (shop/impl.py chooses which one).

CSRF is switched off on purpose to keep the lab short; a real shop needs authentication and CSRF
protection (week 14 onwards).
"""
import json

from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from shop import audit
from shop.catalog import catalog_from_db, save_stock
from shop.domain import CartError, InvalidCoupon, InvalidQuantity, OutOfStock, UnknownProduct
from shop.impl import cart as cart_module

STATUS = {UnknownProduct: 404, OutOfStock: 409, InvalidQuantity: 400, InvalidCoupon: 400, CartError: 400}


def _error(exc):
    status = next(code for cls, code in STATUS.items() if isinstance(exc, cls))
    return JsonResponse({"error": type(exc).__name__, "detail": str(exc)}, status=status)


def _body(request):
    try:
        return json.loads(request.body or b"{}")
    except ValueError:
        raise CartError("El cuerpo no es JSON válido") from None


def _load(request, catalog):
    state = request.session.get("cart")
    if state is None:
        return cart_module.Cart(catalog)
    return cart_module.Cart.from_state(catalog, state)


def _store(request, cart):
    request.session["cart"] = cart.to_state()


@csrf_exempt
@require_http_methods(["GET", "DELETE"])
def cart_detail(request):
    cart = _load(request, catalog_from_db())
    if request.method == "DELETE":
        request.session.pop("cart", None)
        return HttpResponse(status=204)
    return JsonResponse(cart.summary())


@csrf_exempt
@require_http_methods(["POST"])
def cart_add(request):
    cart = _load(request, catalog_from_db())
    try:
        cart_module.add_from_payload(cart, _body(request))
    except CartError as exc:
        return _error(exc)
    _store(request, cart)
    return JsonResponse(cart.summary(), status=201)


@csrf_exempt
@require_http_methods(["DELETE"])
def cart_remove(request, sku):
    cart = _load(request, catalog_from_db())
    raw = request.GET.get("qty")
    try:
        qty = int(raw) if raw is not None else None
        cart.remove(sku, qty)
    except ValueError:
        return _error(InvalidQuantity(f"qty no es un entero: {raw!r}"))
    except CartError as exc:
        return _error(exc)
    _store(request, cart)
    return JsonResponse(cart.summary())


@csrf_exempt
@require_http_methods(["POST"])
def cart_coupon(request):
    cart = _load(request, catalog_from_db())
    try:
        cart.apply_coupon(_body(request).get("code"))
    except CartError as exc:
        return _error(exc)
    _store(request, cart)
    return JsonResponse(cart.summary())


@csrf_exempt
@require_http_methods(["POST"])
def cart_checkout(request):
    with transaction.atomic():
        catalog = catalog_from_db()
        cart = _load(request, catalog)
        try:
            order = cart.checkout()
        except CartError as exc:
            return _error(exc)
        save_stock(catalog)
    request.session.pop("cart", None)
    return JsonResponse(order, status=201)


@csrf_exempt
@require_http_methods(["POST"])
def cart_audit(request):
    """Audit a cart someone else produced: {"items": [...], "coupon": ..., "declared": {...}}."""
    try:
        declared = _body(request)
    except CartError as exc:
        return _error(exc)
    replay = request.GET.get("replay") == "1"
    findings = audit.audit_cart(declared, catalog_from_db(), replay=replay)
    return JsonResponse({"ok": not findings, "findings": [f.as_dict() for f in findings]})
