"""Chooses WHICH cart the tests, the API and the audit use, from the SHOP_MODE variable.

team       your own shop/cart_team.py (default)
ai         shop/cart_ai.py, the cart an AI assistant wrote
solutions  teacher/solutions/cart.py (only exists in the teacher's copy)
"""
import importlib
import os

MODULES = {
    "team": "shop.cart_team",
    "ai": "shop.cart_ai",
    "solutions": "teacher.solutions.cart",
}
MODE = os.environ.get("SHOP_MODE", "team")

if MODE not in MODULES:
    raise RuntimeError(f"SHOP_MODE debe ser uno de {sorted(MODULES)}, no {MODE!r}")
try:
    cart = importlib.import_module(MODULES[MODE])
except ModuleNotFoundError as exc:
    raise RuntimeError(f"El modo «{MODE}» no está disponible en esta copia ({exc.name}).") from exc
