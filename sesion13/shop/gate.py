"""Headless gate for a cart implementation: the agent proposes, the gate decides.

The gate joins two oracles that never open a screen:

1. the test suite (shop/tests), run against the implementation chosen with SHOP_MODE;
2. the audit with replay over carts/*.json. Every declared cart has an EXPECTED outcome for a
   correct implementation: a cart with a bad quantity, an unknown product or more units than the
   stock must be REJECTED; any other cart must give the totals of the reference formula.

This module is pure logic (no Django, no files): the command in
shop/management/commands/gate.py runs the suite and the audit and asks this module for the verdict.
"""

MUST_REJECT = {"BAD_QTY", "UNKNOWN_SKU", "OVER_STOCK"}

RESULTS = {
    "ok": "como se esperaba",
    "sin_implementar": "faltan métodos por implementar",
    "acepta_lo_que_debia_rechazar": "acepta un carrito que debía rechazar",
    "rechaza_un_carrito_valido": "rechaza un carrito válido",
    "calcula_distinto": "calcula totales distintos de la fórmula",
}


def expected_outcome(findings):
    """'rechazar' if the declared cart breaks a quantity or stock rule; otherwise 'totales'."""
    return "rechazar" if any(f["code"] in MUST_REJECT for f in findings) else "totales"


def judge_cart(findings):
    """Return (expected, result) for one cart, from the audit findings with replay."""
    codes = {f["code"] for f in findings}
    declared = [f for f in findings if not f["code"].startswith("REPLAY_")]
    expected = expected_outcome(declared)
    if "REPLAY_UNAVAILABLE" in codes:
        return expected, "sin_implementar"
    rejected = "REPLAY_REJECTED" in codes
    if expected == "rechazar":
        return expected, "ok" if rejected else "acepta_lo_que_debia_rechazar"
    if rejected:
        return expected, "rechaza_un_carrito_valido"
    if "REPLAY_MISMATCH" in codes:
        return expected, "calcula_distinto"
    return expected, "ok"


def verdict(tests_total, tests_failed, carts):
    """Return (verdict, exit code): ('aceptar', 0), ('rechazar', 1) or ('no_disponible', 2)."""
    if not tests_total:
        return "no_disponible", 2
    if tests_failed == 0 and carts and all(c["result"] == "ok" for c in carts):
        return "aceptar", 0
    return "rechazar", 1
