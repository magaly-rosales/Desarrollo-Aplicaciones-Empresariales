"""Cart audit: given a cart somebody else produced, say what does not add up.

A declared cart looks like this (see carts/*.json):

    {"items": [{"sku": "MOU-01", "qty": 2, "unit_price": "39.90"}],
     "coupons": ["BIENVENIDA10"],
     "declared": {"subtotal": "79.80", "discount": "7.98", "igv": "12.93", "total": "84.75"}}

The audit does NOT trust the cart: prices and stock come from the catalog, and the totals are
recomputed with Decimal from the rules in shop/domain.py. With replay=True it also rebuilds the cart
with the ACTIVE implementation (SHOP_MODE) and compares: that is how you audit a cart implementation.
"""
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation

from shop.domain import COUPONS, CartError, reference_totals

FIELDS = ("subtotal", "discount", "igv", "total")


@dataclass
class Finding:
    code: str
    detail: str

    def as_dict(self):
        return {"code": self.code, "detail": self.detail}


def _dec(value):
    try:
        return Decimal(str(value))
    except InvalidOperation:
        return None


def audit_cart(declared, catalog, replay=False):
    """Return a list of Finding (empty = the cart is consistent)."""
    findings = []
    lines = []  # (catalog price, qty) of the lines that can be priced
    totals_by_sku = {}
    for item in declared.get("items", []):
        sku, qty = item.get("sku"), item.get("qty")
        if not isinstance(qty, int) or isinstance(qty, bool) or qty < 1:
            findings.append(Finding("BAD_QTY", f"{sku}: cantidad {qty!r} no válida"))
            continue
        product = catalog.get(sku)
        if product is None:
            findings.append(Finding("UNKNOWN_SKU", f"{sku}: no está en el catálogo"))
            continue
        totals_by_sku[sku] = totals_by_sku.get(sku, 0) + qty
        price = _dec(item.get("unit_price"))
        if price != product.price:
            findings.append(Finding("PRICE_MISMATCH", f"{sku}: el carrito cobra {item.get('unit_price')} y el catálogo dice {product.price}"))
        lines.append((product.price, qty))
    for sku, qty in totals_by_sku.items():
        if qty > catalog[sku].stock:
            findings.append(Finding("OVER_STOCK", f"{sku}: {qty} unidades y solo hay {catalog[sku].stock}"))

    coupons = declared.get("coupons")
    if coupons is None:
        coupons = [declared["coupon"]] if declared.get("coupon") else []
    for code in coupons:
        if code not in COUPONS:
            findings.append(Finding("COUPON_INVALID", f"Cupón desconocido: {code!r}"))
    if len(coupons) > 1:
        findings.append(Finding("MULTIPLE_COUPONS", f"Hay {len(coupons)} cupones y la regla es uno por carrito: {coupons}"))
    valid = [c for c in coupons if c in COUPONS]

    expected = reference_totals(lines, valid)
    for field in FIELDS:
        if field in declared.get("declared", {}):
            got = _dec(declared["declared"][field])
            if got != expected[field]:
                findings.append(Finding("TOTAL_MISMATCH", f"{field}: el carrito declara {declared['declared'][field]} y el cálculo da {expected[field]}"))

    if replay:
        findings.extend(_replay(declared, catalog, valid, expected))
    return findings


def _replay(declared, catalog, coupons, expected):
    """Rebuild the cart with the active implementation and compare it with the reference formula."""
    import copy

    from shop.impl import cart as cart_module

    cart = cart_module.Cart(copy.deepcopy(catalog))
    try:
        for item in declared.get("items", []):
            cart.add(item["sku"], item["qty"])
        for code in coupons:
            cart.apply_coupon(code)
        got = {"subtotal": cart.subtotal(), "discount": cart.discount(), "igv": cart.igv(), "total": cart.total()}
    except CartError as exc:
        return [Finding("REPLAY_REJECTED", f"La implementación activa rechaza el carrito: {exc}")]
    except NotImplementedError as exc:
        return [Finding("REPLAY_UNAVAILABLE", f"Falta implementar {exc}")]
    return [
        Finding("REPLAY_MISMATCH", f"{field}: la implementación da {got[field]} y la fórmula da {expected[field]}")
        for field in FIELDS
        if got[field] != expected[field]
    ]
