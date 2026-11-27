"""Bridge between the Product table and the pure Product dataclass the cart works with."""
from shop.domain import Product as ProductData
from shop.models import Product


def catalog_from_db():
    return {p.sku: ProductData(p.sku, p.name, p.price, p.stock) for p in Product.objects.all()}


def save_stock(catalog):
    """Write back the stock the cart changed (checkout). The CHECK of PositiveIntegerField is the last defense: a negative stock fails here."""
    for sku, data in catalog.items():
        Product.objects.filter(sku=sku).update(stock=data.stock)
