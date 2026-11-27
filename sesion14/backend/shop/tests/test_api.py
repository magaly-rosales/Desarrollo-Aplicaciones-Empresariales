"""Part 5: the API. The server decides the price, the stock and the totals; the client only asks."""
import json

from django.test import TestCase

from shop.models import Product
from shop.seed_data import seed


class ApiTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        seed()

    def post(self, url, body):
        return self.client.post(url, json.dumps(body), content_type="application/json")

    def test_adding_an_item_returns_the_cart(self):
        response = self.post("/api/cart/items/", {"sku": "MOU-01", "qty": 2})
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["subtotal"], "79.80")
        self.assertEqual(data["total"], "94.16")

    def test_the_cart_persists_between_requests(self):
        self.post("/api/cart/items/", {"sku": "MOU-01"})
        self.post("/api/cart/items/", {"sku": "MOU-01"})
        data = self.client.get("/api/cart/").json()
        self.assertEqual([(l["sku"], l["qty"]) for l in data["lines"]], [("MOU-01", 2)])

    def test_the_price_comes_from_the_catalog_not_from_the_client(self):
        response = self.post("/api/cart/items/", {"sku": "LAP-01", "qty": 1, "price": 0.01})
        data = self.client.get("/api/cart/").json()
        self.assertLess(response.status_code, 500)
        self.assertEqual(data["lines"][0]["unit_price"], "2499.90")
        self.assertEqual(data["subtotal"], "2499.90")

    def test_a_negative_price_from_the_client_changes_nothing_either(self):
        self.post("/api/cart/items/", {"sku": "LAP-01", "price": -100})
        self.assertEqual(self.client.get("/api/cart/").json()["subtotal"], "2499.90")

    def test_unknown_product_is_404(self):
        self.assertEqual(self.post("/api/cart/items/", {"sku": "XXX-99"}).status_code, 404)

    def test_more_than_the_stock_is_409(self):
        self.post("/api/cart/items/", {"sku": "PAD-01", "qty": 2})
        response = self.post("/api/cart/items/", {"sku": "PAD-01", "qty": 1})
        self.assertEqual(response.status_code, 409)
        self.assertEqual(self.client.get("/api/cart/").json()["lines"][0]["qty"], 2)

    def test_bad_input_is_400(self):
        for body in ({"sku": "MOU-01", "qty": 0}, {"sku": "MOU-01", "qty": "dos"}, {"qty": 1}, [1, 2]):
            with self.subTest(body=body):
                self.assertEqual(self.post("/api/cart/items/", body).status_code, 400)
        response = self.client.post("/api/cart/items/", "{no es json", content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_remove_more_than_there_is_leaves_no_negative_line(self):
        self.post("/api/cart/items/", {"sku": "MOU-01", "qty": 2})
        response = self.client.delete("/api/cart/items/MOU-01/?qty=5")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["lines"], [])
        self.assertEqual(response.json()["total"], "0.00")

    def test_remove_with_a_quantity_that_is_not_a_number_is_400(self):
        self.post("/api/cart/items/", {"sku": "MOU-01"})
        self.assertEqual(self.client.delete("/api/cart/items/MOU-01/?qty=abc").status_code, 400)

    def test_the_coupon_is_applied_once_even_if_the_client_repeats_it(self):
        self.post("/api/cart/items/", {"sku": "KEY-01"})
        self.post("/api/cart/coupon/", {"code": "BIENVENIDA10"})
        response = self.post("/api/cart/coupon/", {"code": "BIENVENIDA10"})
        self.assertEqual(response.json()["discount"], "18.90")
        self.assertEqual(response.json()["total"], "200.72")

    def test_unknown_coupon_is_400(self):
        self.assertEqual(self.post("/api/cart/coupon/", {"code": "GRATIS100"}).status_code, 400)

    def test_checkout_creates_the_order_and_lowers_the_stock(self):
        self.post("/api/cart/items/", {"sku": "PAD-01", "qty": 2})
        response = self.post("/api/cart/checkout/", {})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["subtotal"], "16.90")
        self.assertEqual(Product.objects.get(sku="PAD-01").stock, 0)
        self.assertEqual(self.client.get("/api/cart/").json()["lines"], [])

    def test_checkout_of_an_empty_cart_is_400(self):
        self.assertEqual(self.post("/api/cart/checkout/", {}).status_code, 400)

    def test_checkout_when_the_stock_changed_is_409_and_keeps_the_cart(self):
        self.post("/api/cart/items/", {"sku": "PAD-01", "qty": 2})
        Product.objects.filter(sku="PAD-01").update(stock=1)  # another customer bought one
        self.assertEqual(self.post("/api/cart/checkout/", {}).status_code, 409)
        self.assertEqual(Product.objects.get(sku="PAD-01").stock, 1)
        self.assertEqual(self.client.get("/api/cart/").json()["lines"][0]["qty"], 2)
