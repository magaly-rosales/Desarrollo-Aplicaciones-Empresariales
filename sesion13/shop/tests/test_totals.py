"""Part 3: money. Subtotal, tax and total with Decimal, rounding half up."""
from decimal import Decimal
from unittest import TestCase

from shop.impl import cart as impl
from shop.seed_data import catalog_data


class TotalsTests(TestCase):
    def setUp(self):
        self.cart = impl.Cart(catalog_data())

    def test_subtotal_is_the_sum_of_price_times_quantity(self):
        self.cart.add("MOU-01", 2)  # 79.80
        self.cart.add("KEY-01", 1)  # 189.00
        self.assertEqual(self.cart.subtotal(), Decimal("268.80"))

    def test_igv_and_total_without_coupon(self):
        self.cart.add("MOU-01", 2)
        self.cart.add("KEY-01", 1)
        self.assertEqual(self.cart.discount(), Decimal("0.00"))
        self.assertEqual(self.cart.igv(), Decimal("48.38"))  # 268.80 * 0.18 = 48.384
        self.assertEqual(self.cart.total(), Decimal("317.18"))

    def test_money_is_decimal_not_float(self):
        self.cart.add("MOU-01")
        for value in (self.cart.subtotal(), self.cart.discount(), self.cart.igv(), self.cart.total()):
            self.assertIsInstance(value, Decimal)

    def test_ten_small_items_add_up_exactly(self):
        self.cart.add("STK-01", 3)  # 3 * 0.35: the classic 0.1 + 0.2 problem
        self.assertEqual(self.cart.subtotal(), Decimal("1.05"))
        self.assertEqual(self.cart.total(), Decimal("1.24"))  # 1.05 + 0.19 (0.189)

    def test_igv_rounds_half_up(self):
        self.cart.add("LAP-01")
        self.cart.add("CAB-01")  # 2512.25 * 0.18 = 452.205 exactly
        self.assertEqual(self.cart.igv(), Decimal("452.21"))
        self.assertEqual(self.cart.total(), Decimal("2964.46"))

    def test_the_discount_rounds_half_up(self):
        self.cart.add("PAD-01")  # 8.45 * 10 % = 0.845 exactly
        self.cart.apply_coupon("BIENVENIDA10")
        self.assertEqual(self.cart.discount(), Decimal("0.85"))
        self.assertEqual(self.cart.total(), Decimal("8.97"))

    def test_a_discount_of_one_and_a_half_cents(self):
        self.cart.add("STK-01", 3)  # 1.05 * 10 % = 0.105 exactly
        self.cart.apply_coupon("BIENVENIDA10")
        self.assertEqual(self.cart.discount(), Decimal("0.11"))

    def test_total_is_the_sum_of_its_rounded_parts(self):
        self.cart.add("HUB-01")  # 67.45
        self.cart.apply_coupon("BIENVENIDA10")  # discount 6.745 -> 6.75, base 60.70
        self.assertEqual(self.cart.subtotal() - self.cart.discount() + self.cart.igv(), self.cart.total())
        self.assertEqual(self.cart.total(), Decimal("71.63"))

    def test_summary_has_the_shape_the_api_sends(self):
        self.cart.add("MOU-01", 2)
        self.cart.apply_coupon("BIENVENIDA10")
        self.assertEqual(self.cart.summary(), {
            "lines": [{"sku": "MOU-01", "name": "Mouse inalámbrico", "unit_price": "39.90", "qty": 2,
                       "line_total": "79.80"}],
            "coupon": "BIENVENIDA10",
            "subtotal": "79.80",
            "discount": "7.98",
            "igv": "12.93",
            "total": "84.75",
        })

    def test_summary_of_an_empty_cart(self):
        self.assertEqual(self.cart.summary(), {
            "lines": [], "coupon": None, "subtotal": "0.00", "discount": "0.00", "igv": "0.00", "total": "0.00",
        })
