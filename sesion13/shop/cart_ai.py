"""Shopping cart written by an AI assistant (version under review)."""
from decimal import Decimal

from shop.domain import (
    COUPONS,
    CartError,
    InvalidCoupon,
    InvalidQuantity,
    Line,
    OutOfStock,
    UnknownProduct,
)

IGV = 0.18


def _money(value):
    return Decimal(str(round(value, 2)))


def _check_qty(qty):
    if isinstance(qty, bool) or not isinstance(qty, int) or qty < 1:
        raise InvalidQuantity(f"Cantidad no válida: {qty!r}")


class Cart:
    def __init__(self, catalog):
        self._catalog = catalog
        self._qty = {}
        self._prices = {}
        self._coupons = []

    def to_state(self):
        return {"qty": dict(self._qty), "prices": {k: str(v) for k, v in self._prices.items()},
                "coupons": list(self._coupons)}

    @classmethod
    def from_state(cls, catalog, state):
        cart = cls(catalog)
        cart._qty = {sku: int(q) for sku, q in state.get("qty", {}).items() if sku in catalog}
        cart._prices = {k: Decimal(v) for k, v in state.get("prices", {}).items() if k in cart._qty}
        cart._coupons = list(state.get("coupons", []))
        return cart

    def add(self, sku, qty=1, price=None):
        _check_qty(qty)
        product = self._catalog.get(sku)
        if product is None:
            raise UnknownProduct(f"No existe el producto {sku!r}")
        if qty > product.stock:
            raise OutOfStock(f"{sku}: pides {qty} y quedan {product.stock}")
        self._qty[sku] = self._qty.get(sku, 0) + qty
        self._prices[sku] = Decimal(str(price)) if price is not None else product.price

    def remove(self, sku, qty=None):
        if sku not in self._qty:
            raise UnknownProduct(f"{sku!r} no está en el carrito")
        if qty is None:
            del self._qty[sku]
            del self._prices[sku]
            return
        _check_qty(qty)
        self._qty[sku] -= qty
        if self._qty[sku] == 0:
            del self._qty[sku]
            del self._prices[sku]

    def qty_of(self, sku):
        return self._qty.get(sku, 0)

    def lines(self):
        return [
            Line(sku, self._catalog[sku].name, self._prices[sku], qty)
            for sku, qty in self._qty.items()
        ]

    def apply_coupon(self, code):
        code = (code or "").strip().upper()
        if code not in COUPONS:
            raise InvalidCoupon(f"Cupón desconocido: {code!r}")
        self._coupons.append(code)

    def _subtotal(self):
        return sum(float(l.unit_price) * l.qty for l in self.lines())

    def _discount(self):
        subtotal = self._subtotal()
        total_discount = 0.0
        for code in self._coupons:
            kind, amount = COUPONS[code]
            if kind == "percent":
                total_discount += subtotal * float(amount) / 100
            else:
                total_discount += min(float(amount), subtotal)
        return total_discount

    def subtotal(self):
        return _money(self._subtotal())

    def discount(self):
        return _money(self._discount())

    def igv(self):
        return _money((self._subtotal() - self._discount()) * IGV)

    def total(self):
        base = self._subtotal() - self._discount()
        return _money(base) + self.igv()

    def summary(self):
        return {
            "lines": [
                {"sku": l.sku, "name": l.name, "unit_price": f"{l.unit_price:.2f}", "qty": l.qty,
                 "line_total": f"{l.total:.2f}"}
                for l in self.lines()
            ],
            "coupon": self._coupons[-1] if self._coupons else None,
            "subtotal": f"{self.subtotal():.2f}",
            "discount": f"{self.discount():.2f}",
            "igv": f"{self.igv():.2f}",
            "total": f"{self.total():.2f}",
        }

    def checkout(self):
        if not self._qty:
            raise CartError("El carrito está vacío")
        order = self.summary()
        for sku, qty in self._qty.items():
            self._catalog[sku].stock -= qty
        self._qty = {}
        self._prices = {}
        self._coupons = []
        return order


def add_from_payload(cart, payload):
    if not isinstance(payload, dict) or not isinstance(payload.get("sku"), str):
        raise CartError("Falta el campo «sku»")
    cart.add(payload["sku"], payload.get("qty", 1), payload.get("price"))
