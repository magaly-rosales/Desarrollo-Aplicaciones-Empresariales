"""Part 1: the lines of the cart (add, remove, quantities)."""
from decimal import Decimal
from unittest import TestCase

from shop.domain import CartError, InvalidQuantity, UnknownProduct
from shop.impl import cart as impl
from shop.seed_data import catalog_data


class LinesTests(TestCase):
    def setUp(self):
        self.cart = impl.Cart(catalog_data())

    def test_new_cart_is_empty(self):
        self.assertEqual(self.cart.lines(), [])
        self.assertEqual(self.cart.total(), Decimal("0.00"))

    def test_add_creates_a_line_with_the_catalog_price(self):
        self.cart.add("MOU-01", 2)
        [line] = self.cart.lines()
        self.assertEqual((line.sku, line.name, line.unit_price, line.qty),
                         ("MOU-01", "Mouse inalámbrico", Decimal("39.90"), 2))
        self.assertEqual(line.total, Decimal("79.80"))

    def test_add_defaults_to_one_unit(self):
        self.cart.add("KEY-01")
        self.assertEqual(self.cart.qty_of("KEY-01"), 1)

    def test_adding_the_same_product_accumulates(self):
        self.cart.add("MOU-01", 2)
        self.cart.add("MOU-01", 3)
        self.assertEqual(self.cart.qty_of("MOU-01"), 5)
        self.assertEqual(len(self.cart.lines()), 1)

    def test_lines_keep_insertion_order(self):
        for sku in ("HUB-01", "CAB-01", "MOU-01"):
            self.cart.add(sku)
        self.assertEqual([l.sku for l in self.cart.lines()], ["HUB-01", "CAB-01", "MOU-01"])

    def test_invalid_quantities_are_rejected(self):
        for bad in (0, -1, 2.5, "2", None, True):
            with self.subTest(qty=bad):
                with self.assertRaises(InvalidQuantity):
                    self.cart.add("MOU-01", bad)
        self.assertEqual(self.cart.lines(), [])

    def test_unknown_product_is_rejected(self):
        with self.assertRaises(UnknownProduct):
            self.cart.add("XXX-99")

    def test_remove_without_quantity_drops_the_line(self):
        self.cart.add("MOU-01", 3)
        self.cart.remove("MOU-01")
        self.assertEqual(self.cart.qty_of("MOU-01"), 0)
        self.assertEqual(self.cart.lines(), [])

    def test_remove_some_units_keeps_the_rest(self):
        self.cart.add("MOU-01", 5)
        self.cart.remove("MOU-01", 2)
        self.assertEqual(self.cart.qty_of("MOU-01"), 3)

    def test_remove_exactly_what_is_there_drops_the_line(self):
        self.cart.add("MOU-01", 2)
        self.cart.remove("MOU-01", 2)
        self.assertEqual(self.cart.lines(), [])

    def test_remove_more_than_there_is_never_leaves_a_negative_quantity(self):
        self.cart.add("MOU-01", 2)
        self.cart.remove("MOU-01", 5)
        self.assertEqual(self.cart.qty_of("MOU-01"), 0)
        self.assertEqual(self.cart.lines(), [])
        self.assertEqual(self.cart.total(), Decimal("0.00"))

    def test_remove_something_that_is_not_in_the_cart(self):
        with self.assertRaises(UnknownProduct):
            self.cart.remove("MOU-01")

    def test_remove_with_an_invalid_quantity(self):
        self.cart.add("MOU-01", 2)
        for bad in (0, -1):
            with self.subTest(qty=bad):
                with self.assertRaises(InvalidQuantity):
                    self.cart.remove("MOU-01", bad)
        self.assertEqual(self.cart.qty_of("MOU-01"), 2)

    def test_errors_share_a_base_class(self):
        with self.assertRaises(CartError):
            self.cart.add("XXX-99")

    def test_state_survives_between_requests(self):
        self.cart.add("MOU-01", 2)
        self.cart.add("KEY-01")
        self.cart.apply_coupon("BIENVENIDA10")
        again = impl.Cart.from_state(catalog_data(), self.cart.to_state())
        self.assertEqual(again.summary(), self.cart.summary())
