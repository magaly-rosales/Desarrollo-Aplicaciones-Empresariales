"""Your cart. Complete every TODO until `python manage.py test` is green.

The rules (money, stock, coupons, checkout) are in README.md and in shop/domain.py. Do not change
shop/domain.py or the tests. Money is Decimal (never float) and the price always comes from the
catalog, never from the request.
"""
from decimal import Decimal  # noqa: F401

from shop.domain import (  # noqa: F401  (you will need most of these)
    COUPONS,
    IGV_RATE,
    CartError,
    InvalidCoupon,
    InvalidQuantity,
    Line,
    OutOfStock,
    UnknownProduct,
    fmt,
    money,
)


class Cart:
    def __init__(self, catalog):
        self._catalog = catalog  # sku -> Product (price Decimal, stock int)
        self._qty = {}  # sku -> quantity, in insertion order
        self._coupon = None  # one coupon per cart

    # --- persistence between requests (already done) ---
    def to_state(self):
        return {"qty": dict(self._qty), "coupon": self._coupon}

    @classmethod
    def from_state(cls, catalog, state):
        cart = cls(catalog)
        cart._qty = {sku: int(q) for sku, q in state.get("qty", {}).items() if sku in catalog}
        cart._coupon = state.get("coupon")
        return cart

    # --- lines ---
    def add(self, sku, qty=1):
        """qty is an int >= 1 (InvalidQuantity); the sku exists (UnknownProduct);
        what is already in the cart plus qty must not exceed the stock (OutOfStock, cart unchanged)."""
        if not isinstance(qty, int) or isinstance(qty, bool) or qty < 1:
            raise InvalidQuantity(f"qty must be an integer >= 1, got {qty!r}")
        if sku not in self._catalog:
            raise UnknownProduct(f"SKU {sku!r} not in catalog")
        current = self._qty.get(sku, 0)
        if current + qty > self._catalog[sku].stock:
            raise OutOfStock(f"SKU {sku!r}: have {current}, want {qty}, stock {self._catalog[sku].stock}")
        self._qty[sku] = current + qty

    def remove(self, sku, qty=None):
        """qty=None removes the whole line; otherwise subtract qty and drop the line when it
        reaches zero. A sku that is not in the cart is UnknownProduct. Never leave a negative quantity."""
        if sku not in self._qty:
            raise UnknownProduct(f"SKU {sku!r} not in cart")
        if qty is None:
            del self._qty[sku]
            return
        if not isinstance(qty, int) or isinstance(qty, bool) or qty < 1:
            raise InvalidQuantity(f"qty must be an integer >= 1, got {qty!r}")
        current = self._qty[sku]
        new_qty = current - qty
        if new_qty <= 0:
            del self._qty[sku]
        else:
            self._qty[sku] = new_qty

    def qty_of(self, sku):
        return self._qty.get(sku, 0)

    def lines(self):
        """one Line(sku, name, unit_price, qty) per sku, in insertion order, price from the catalog."""
        result = []
        for sku, qty in self._qty.items():
            product = self._catalog[sku]
            result.append(Line(sku=sku, name=product.name, unit_price=product.price, qty=qty))
        return result

    # --- coupon and totals ---
    def apply_coupon(self, code):
        """code without spaces and in upper case; unknown -> InvalidCoupon. One coupon per cart:
        applying again (the same or another) REPLACES it."""
        normalized = code.strip().upper()
        if normalized not in COUPONS:
            raise InvalidCoupon(f"Unknown coupon {normalized!r}")
        self._coupon = normalized

    def subtotal(self):
        """sum of price * qty, rounded to cents (Decimal)."""
        return money(sum(
            (self._catalog[sku].price * qty for sku, qty in self._qty.items()),
            Decimal("0"),
        ))

    def discount(self):
        """percent coupon = subtotal * pct / 100 rounded half up; fixed coupon = the amount, but
        never more than the subtotal; no coupon = Decimal('0.00')."""
        if not self._coupon:
            return Decimal("0.00")
        kind, amount = COUPONS[self._coupon]
        sub = self.subtotal()
        if kind == "percent":
            return money(sub * amount / Decimal("100"))
        elif kind == "fixed":
            return min(amount, sub)

    def igv(self):
        """18 % of (subtotal - discount), rounded half up."""
        return money((self.subtotal() - self.discount()) * IGV_RATE)

    def total(self):
        """(subtotal - discount) + igv."""
        return (self.subtotal() - self.discount()) + self.igv()

    def summary(self):
        """the dict the API returns. Keys: lines (list of dicts with sku, name, unit_price,
        qty, line_total as 2-decimal strings), coupon, subtotal, discount, igv, total (strings via fmt)."""
        lines = []
        for line in self.lines():
            lines.append({
                "sku": line.sku,
                "name": line.name,
                "unit_price": fmt(line.unit_price),
                "qty": line.qty,
                "line_total": fmt(line.total),
            })
        return {
            "lines": lines,
            "coupon": self._coupon,
            "subtotal": fmt(self.subtotal()),
            "discount": fmt(self.discount()),
            "igv": fmt(self.igv()),
            "total": fmt(self.total()),
        }

    # --- checkout ---
    def checkout(self):
        """TODO: empty cart -> CartError; stock is checked AGAIN (OutOfStock); on success the catalog stock
        goes down by what was bought, the cart is emptied and the summary of the order is returned."""
        raise NotImplementedError("TODO: checkout")


def add_from_payload(cart, payload):
    """Translate the JSON body of POST /api/cart/items/ ({"sku": ..., "qty": ...}) into a cart.add
    call. The body is untrusted: if it is not a dict with a string «sku», raise CartError. The price is
    NOT part of the contract: the catalog is the only source of prices."""
    if not isinstance(payload, dict):
        raise CartError("payload must be a dict")
    if "sku" not in payload or not isinstance(payload["sku"], str):
        raise CartError("payload must contain a string 'sku'")
    qty = payload.get("qty", 1)
    return cart.add(payload["sku"], qty)
