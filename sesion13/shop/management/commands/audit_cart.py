import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from shop import audit
from shop.catalog import catalog_from_db
from shop.impl import MODE
from shop.seed_data import catalog_data


class Command(BaseCommand):
    help = "Audita un carrito declarado en un archivo JSON (modo headless, sin pantalla)."

    def add_arguments(self, parser):
        parser.add_argument("paths", nargs="+", help="uno o más archivos JSON (por ejemplo carts/*.json)")
        parser.add_argument("--replay", action="store_true",
                            help="además reconstruye el carrito con la implementación activa (SHOP_MODE)")
        parser.add_argument("--json", action="store_true", help="salida en JSON, para otro programa o un agente")
        parser.add_argument("--strict", action="store_true", help="terminar con error si algún carrito tiene hallazgos")
        parser.add_argument("--catalogo-fijo", action="store_true",
                            help="usar el catálogo fijo de seed_data, sin la base de datos (resultado siempre igual)")

    def handle(self, *args, **options):
        catalog = catalog_data() if options["catalogo_fijo"] else catalog_from_db()
        if not catalog:
            raise CommandError("El catálogo está vacío: ejecuta primero «python manage.py seed_shop».")
        report, dirty = [], 0
        for raw in options["paths"]:
            path = Path(raw)
            try:
                declared = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, ValueError) as exc:
                raise CommandError(f"No pude leer {path}: {exc}") from exc
            findings = audit.audit_cart(declared, catalog, replay=options["replay"])
            dirty += bool(findings)
            report.append({"file": path.name, "ok": not findings, "findings": [f.as_dict() for f in findings]})

        if options["json"]:
            self.stdout.write(json.dumps({"mode": MODE, "carts": report}, ensure_ascii=False, indent=2))
        else:
            self.stdout.write(f"\nAuditoría de carritos (implementación activa: {MODE})\n")
            for entry in report:
                self.stdout.write(f"{'OK  ' if entry['ok'] else 'FALLA'} {entry['file']}")
                for f in entry["findings"]:
                    self.stdout.write(f"      {f['code']:<16} {f['detail']}")
            self.stdout.write(f"\n{len(report) - dirty} de {len(report)} carritos sin hallazgos.\n")
        if options["strict"] and dirty:
            raise CommandError(f"{dirty} carrito(s) con hallazgos.")
