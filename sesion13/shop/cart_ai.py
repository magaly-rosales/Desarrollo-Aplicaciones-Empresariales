"""Shopping cart written by an AI assistant (version under review)."""
from decimal import Decimal

from shop.domain import (
    COUPONS,
    CartError,
    IGV_RATE,
    InvalidCoupon,
    InvalidQuantity,
    Line,
    OutOfStock,
    UnknownProduct,
    money,
)


def _check_qty(qty):
    if isinstance(qty, bool) or not isinstance(qty, int) or qty < 1:
        raise InvalidQuantity(f"Cantidad no válida: {qty!r}")


class Cart:
    def __init__(self, catalog):
        self._catalog = catalog
        self._qty = {}
        self._coupons = []

    def to_state(self):
        return {"qty": dict(self._qty), "coupons": list(self._coupons)}

    @classmethod
    def from_state(cls, catalog, state):
        cart = cls(catalog)
        cart._qty = {sku: int(q) for sku, q in state.get("qty", {}).items() if sku in catalog}
        cart._coupons = list(state.get("coupons", []))
        return cart

    def add(self, sku, qty=1):
        _check_qty(qty)
        product = self._catalog.get(sku)
        if product is None:
            raise UnknownProduct(f"No existe el producto {sku!r}")
        requested_qty = self._qty.get(sku, 0) + qty
        if requested_qty > product.stock:
            raise OutOfStock(f"{sku}: pides {requested_qty} y quedan {product.stock}")
        self._qty[sku] = self._qty.get(sku, 0) + qty

    def remove(self, sku, qty=None):
        if sku not in self._qty:
            raise UnknownProduct(f"{sku!r} no está en el carrito")
        if qty is None:
            del self._qty[sku]
            return
        _check_qty(qty)
        remaining_qty = self._qty[sku] - qty
        if remaining_qty <= 0:
            del self._qty[sku]
        else:
            self._qty[sku] = remaining_qty

    def qty_of(self, sku):
        return self._qty.get(sku, 0)

    def lines(self):
        return [
            Line(sku, self._catalog[sku].name, self._catalog[sku].price, qty)
            for sku, qty in self._qty.items()
        ]

    def apply_coupon(self, code):
        if not isinstance(code, str):
            raise InvalidCoupon(f"Cupón desconocido: {code!r}")
        code = code.strip().upper()
        if code not in COUPONS:
            raise InvalidCoupon(f"Cupón desconocido: {code!r}")
        self._coupons = [code]

    def _subtotal(self):
        return sum((l.unit_price * l.qty for l in self.lines()), Decimal("0"))

    def _discount(self):
        subtotal = self._subtotal()
        if not self._coupons:
            return Decimal("0")
        kind, amount = COUPONS[self._coupons[-1]]
        if kind == "percent":
            return subtotal * amount / Decimal("100")
        return min(amount, subtotal)

    def subtotal(self):
        return money(self._subtotal())

    def discount(self):
        return money(self._discount())

    def igv(self):
        return money((self._subtotal() - self.discount()) * IGV_RATE)

    def total(self):
        base = self._subtotal() - self.discount()
        return money(base) + self.igv()

    def summary(self):
        coupon = self._coupons[-1] if self._coupons else None
        return {
            "lines": [
                {"sku": l.sku, "name": l.name, "unit_price": f"{l.unit_price:.2f}", "qty": l.qty,
                 "line_total": f"{l.total:.2f}"}
                for l in self.lines()
            ],
            "coupon": coupon,
            "subtotal": f"{self.subtotal():.2f}",
            "discount": f"{self.discount():.2f}",
            "igv": f"{self.igv():.2f}",
            "total": f"{self.total():.2f}",
        }

    def checkout(self):
        if not self._qty:
            raise CartError("El carrito está vacío")
        for sku, qty in self._qty.items():
            product = self._catalog[sku]
            if qty > product.stock:
                raise OutOfStock(f"{sku}: pides {qty} y quedan {product.stock}")
        order = self.summary()
        for sku, qty in self._qty.items():
            self._catalog[sku].stock -= qty
        self._qty = {}
        self._coupons = []
        return order


def add_from_payload(cart, payload):
    if not isinstance(payload, dict) or not isinstance(payload.get("sku"), str):
        raise CartError("Falta el campo «sku»")
    cart.add(payload["sku"], payload.get("qty", 1))
