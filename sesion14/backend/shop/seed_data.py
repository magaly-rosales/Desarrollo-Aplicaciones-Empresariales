"""Fixed catalog: the same data every time, so the right answer to every test is known in advance."""
from decimal import Decimal

from shop.domain import Product as ProductData

PRODUCTS = [
    # sku, name, price, stock
    ("LAP-01", "Laptop 14 pulgadas", "2499.90", 3),
    ("MOU-01", "Mouse inalámbrico", "39.90", 20),
    ("KEY-01", "Teclado mecánico", "189.00", 5),
    ("CAB-01", "Cable HDMI 2 m", "12.35", 50),
    ("USB-01", "Memoria USB 64 GB", "24.99", 10),
    ("PAD-01", "Mousepad", "8.45", 2),
    ("STK-01", "Pegatina", "0.35", 100),
    ("HUB-01", "Hub USB-C", "67.45", 4),
]


def catalog_data():
    """Fresh dict sku -> Product (pure data), without touching the database."""
    return {sku: ProductData(sku, name, Decimal(price), stock) for sku, name, price, stock in PRODUCTS}


def seed():
    """Delete and reload the Product table with PRODUCTS."""
    from shop.models import Product

    Product.objects.all().delete()
    Product.objects.bulk_create(
        Product(sku=sku, name=name, price=Decimal(price), stock=stock) for sku, name, price, stock in PRODUCTS
    )
