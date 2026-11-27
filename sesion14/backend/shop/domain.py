"""Rules and types shared by the three cart implementations (team, ai, solutions).

Everything here is the CONTRACT: the tests and the audit rely on it, so the implementations
must not change it. The rules in plain Spanish are in the README.
"""
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

CENT = Decimal("0.01")
IGV_RATE = Decimal("0.18")  # sales tax (Peru), added AFTER the discount

# One coupon per cart. ("percent", 10) = 10 % of the subtotal; ("fixed", 20) = S/ 20 off, never more
# than the subtotal.
COUPONS = {
    "BIENVENIDA10": ("percent", Decimal("10")),
    "MENOS20": ("fixed", Decimal("20")),
}


class CartError(Exception):
    """Base class of every rule violation."""


class UnknownProduct(CartError):
    pass


class InvalidQuantity(CartError):
    pass


class OutOfStock(CartError):
    pass


class InvalidCoupon(CartError):
    pass


@dataclass
class Product:
    """Catalog entry as the cart sees it (pure data, no database)."""

    sku: str
    name: str
    price: Decimal
    stock: int


@dataclass(frozen=True)
class Line:
    sku: str
    name: str
    unit_price: Decimal
    qty: int

    @property
    def total(self) -> Decimal:
        return self.unit_price * self.qty


def money(value: Decimal) -> Decimal:
    """Round to cents, half up (the rule every shop uses: 0.005 -> 0.01)."""
    return value.quantize(CENT, rounding=ROUND_HALF_UP)


def fmt(value) -> str:
    """Two-decimal string, the way the API sends money."""
    return f"{Decimal(value):.2f}"


def reference_totals(lines, coupons):
    """Subtotal, discount, igv and total from (unit_price, qty) pairs and a list of coupon codes.

    Independent of any Cart: this is the formula in the README, used by the audit.
    Only the first valid coupon counts (one coupon per cart).
    """
    subtotal = sum((Decimal(price) * qty for price, qty in lines), Decimal("0"))
    discount = Decimal("0")
    for code in coupons[:1]:
        kind, amount = COUPONS.get(code, (None, None))
        if kind == "percent":
            discount = money(subtotal * amount / 100)
        elif kind == "fixed":
            discount = min(amount, subtotal)
    base = subtotal - discount
    igv = money(base * IGV_RATE)
    return {"subtotal": money(subtotal), "discount": discount, "igv": igv, "total": money(base) + igv}
