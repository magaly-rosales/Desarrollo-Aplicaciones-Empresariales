"""Part 6: the audit tool (given). It does not depend on your cart, except for --replay."""
import json
from pathlib import Path

from django.core.management import call_command
from django.test import TestCase

from shop.audit import audit_cart
from shop.catalog import catalog_from_db
from shop.seed_data import seed

CARTS = Path(__file__).resolve().parents[2] / "carts"


def load(name):
    return json.loads((CARTS / name).read_text(encoding="utf-8"))


class AuditTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        seed()

    def codes(self, name, replay=False):
        return sorted({f.code for f in audit_cart(load(name), catalog_from_db(), replay=replay)})

    def test_a_consistent_cart_has_no_findings(self):
        self.assertEqual(self.codes("01-correcto.json"), [])

    def test_price_taken_from_the_client(self):
        self.assertEqual(self.codes("02-precio-del-cliente.json"), ["PRICE_MISMATCH", "TOTAL_MISMATCH"])

    def test_more_units_than_the_stock(self):
        self.assertEqual(self.codes("03-stock.json"), ["OVER_STOCK"])

    def test_negative_quantity(self):
        self.assertEqual(self.codes("04-cantidad-negativa.json"), ["BAD_QTY", "TOTAL_MISMATCH"])

    def test_coupon_applied_twice(self):
        self.assertEqual(self.codes("05-cupon-doble.json"), ["MULTIPLE_COUPONS", "TOTAL_MISMATCH"])

    def test_float_rounding(self):
        self.assertEqual(self.codes("06-redondeo.json"), ["TOTAL_MISMATCH"])

    def test_replay_of_a_consistent_cart_matches_your_cart(self):
        # needs a working Cart: red with the skeleton
        self.assertEqual(self.codes("01-correcto.json", replay=True), [])

    def test_replay_of_the_rounding_cart_matches_your_cart(self):
        # the declared totals are wrong, but the REPLAY compares the implementation, not the declaration
        self.assertEqual([c for c in self.codes("06-redondeo.json", replay=True) if c.startswith("REPLAY")], [])

    def test_the_command_reports_in_json(self):
        from io import StringIO

        out = StringIO()
        call_command("audit_cart", str(CARTS / "03-stock.json"), "--json", stdout=out)
        report = json.loads(out.getvalue())
        self.assertFalse(report["carts"][0]["ok"])
        self.assertEqual(report["carts"][0]["findings"][0]["code"], "OVER_STOCK")
