"""Part 4: coupons. One coupon per cart; the discount is never applied twice."""
from decimal import Decimal
from unittest import TestCase

from shop.domain import InvalidCoupon
from shop.impl import cart as impl
from shop.seed_data import catalog_data


class CouponTests(TestCase):
    def setUp(self):
        self.cart = impl.Cart(catalog_data())
        self.cart.add("KEY-01")  # 189.00

    def test_percent_coupon(self):
        self.cart.apply_coupon("BIENVENIDA10")
        self.assertEqual(self.cart.discount(), Decimal("18.90"))
        self.assertEqual(self.cart.igv(), Decimal("30.62"))  # 170.10 * 0.18 = 30.618
        self.assertEqual(self.cart.total(), Decimal("200.72"))

    def test_fixed_coupon(self):
        self.cart.apply_coupon("MENOS20")
        self.assertEqual(self.cart.discount(), Decimal("20.00"))
        self.assertEqual(self.cart.total(), Decimal("199.42"))  # 169.00 + 30.42

    def test_fixed_coupon_never_exceeds_the_subtotal(self):
        cart = impl.Cart(catalog_data())
        cart.add("STK-01", 2)  # 0.70
        cart.apply_coupon("MENOS20")
        self.assertEqual(cart.discount(), Decimal("0.70"))
        self.assertEqual(cart.total(), Decimal("0.00"))

    def test_unknown_coupon_is_rejected_and_changes_nothing(self):
        with self.assertRaises(InvalidCoupon):
            self.cart.apply_coupon("GRATIS100")
        self.assertEqual(self.cart.discount(), Decimal("0.00"))

    def test_code_is_trimmed_and_case_insensitive(self):
        self.cart.apply_coupon("  bienvenida10 ")
        self.assertEqual(self.cart.discount(), Decimal("18.90"))

    def test_applying_the_same_coupon_twice_discounts_once(self):
        self.cart.apply_coupon("BIENVENIDA10")
        self.cart.apply_coupon("BIENVENIDA10")
        self.assertEqual(self.cart.discount(), Decimal("18.90"))
        self.assertEqual(self.cart.total(), Decimal("200.72"))

    def test_a_second_coupon_replaces_the_first(self):
        self.cart.apply_coupon("BIENVENIDA10")
        self.cart.apply_coupon("MENOS20")
        self.assertEqual(self.cart.discount(), Decimal("20.00"))
        self.assertEqual(self.cart.summary()["coupon"], "MENOS20")

    def test_the_discount_follows_the_cart(self):
        self.cart.apply_coupon("BIENVENIDA10")
        self.cart.add("MOU-01")  # subtotal 228.90
        self.assertEqual(self.cart.discount(), Decimal("22.89"))
        self.cart.remove("MOU-01")
        self.assertEqual(self.cart.discount(), Decimal("18.90"))

    def test_no_coupon_no_discount(self):
        self.assertEqual(self.cart.discount(), Decimal("0.00"))
        self.assertIsNone(self.cart.summary()["coupon"])
