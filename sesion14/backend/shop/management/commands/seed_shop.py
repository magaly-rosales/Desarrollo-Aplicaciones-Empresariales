from django.core.management.base import BaseCommand

from shop.seed_data import PRODUCTS, seed


class Command(BaseCommand):
    help = "Borra y vuelve a cargar el catálogo de la tienda (siempre los mismos ocho productos)."

    def handle(self, *args, **options):
        seed()
        self.stdout.write(f"Catálogo cargado: {len(PRODUCTS)} productos.")
