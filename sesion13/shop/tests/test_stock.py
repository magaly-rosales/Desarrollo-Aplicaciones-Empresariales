"""Part 2: stock and checkout. The stock never goes below zero."""
from decimal import Decimal
from unittest import TestCase

from shop.domain import CartError, OutOfStock
from shop.impl import cart as impl
from shop.seed_data import catalog_data


class StockTests(TestCase):
    def setUp(self):
        self.catalog = catalog_data()  # PAD-01 has 2 units, LAP-01 has 3
        self.cart = impl.Cart(self.catalog)

    def test_you_can_add_up_to_the_stock(self):
        self.cart.add("PAD-01", 2)
        self.assertEqual(self.cart.qty_of("PAD-01"), 2)

    def test_more_than_the_stock_is_rejected_and_the_cart_is_unchanged(self):
        with self.assertRaises(OutOfStock):
            self.cart.add("PAD-01", 3)
        self.assertEqual(self.cart.qty_of("PAD-01"), 0)

    def test_the_stock_counts_what_is_already_in_the_cart(self):
        self.cart.add("PAD-01", 2)
        with self.assertRaises(OutOfStock):
            self.cart.add("PAD-01", 1)
        self.assertEqual(self.cart.qty_of("PAD-01"), 2)

    def test_two_adds_cannot_get_around_the_stock(self):
        self.cart.add("LAP-01", 2)
        with self.assertRaises(OutOfStock):
            self.cart.add("LAP-01", 2)
        self.assertEqual(self.cart.qty_of("LAP-01"), 2)

    def test_removing_frees_room_to_add_again(self):
        self.cart.add("PAD-01", 2)
        self.cart.remove("PAD-01", 1)
        self.cart.add("PAD-01", 1)
        self.assertEqual(self.cart.qty_of("PAD-01"), 2)

    def test_checkout_lowers_the_stock_and_empties_the_cart(self):
        self.cart.add("PAD-01", 2)
        self.cart.add("MOU-01", 5)
        order = self.cart.checkout()
        self.assertEqual(self.catalog["PAD-01"].stock, 0)
        self.assertEqual(self.catalog["MOU-01"].stock, 15)
        self.assertEqual(self.cart.lines(), [])
        self.assertEqual(order["subtotal"], "216.40")
        self.assertEqual(order["total"], "255.35")

    def test_checkout_of_an_empty_cart_is_an_error(self):
        with self.assertRaises(CartError):
            self.cart.checkout()

    def test_checkout_checks_the_stock_again(self):
        # someone else bought the same units between "add" and "checkout"
        self.cart.add("PAD-01", 2)
        self.catalog["PAD-01"].stock = 1
        with self.assertRaises(OutOfStock):
            self.cart.checkout()
        self.assertEqual(self.catalog["PAD-01"].stock, 1)
        self.assertEqual(self.cart.qty_of("PAD-01"), 2)  # the cart is not lost

    def test_the_stock_is_never_negative_after_any_sequence(self):
        for qty in (1, 1, 1, 1):
            try:
                self.cart.add("PAD-01", qty)
            except OutOfStock:
                pass
        self.cart.checkout()
        self.assertGreaterEqual(self.catalog["PAD-01"].stock, 0)
        self.assertEqual(self.catalog["PAD-01"].stock, 0)

    def test_checkout_clears_the_coupon(self):
        self.cart.add("MOU-01")
        self.cart.apply_coupon("MENOS20")
        self.cart.checkout()
        self.assertEqual(self.cart.discount(), Decimal("0.00"))
