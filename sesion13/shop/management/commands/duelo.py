import os
import re
import subprocess
import sys
from pathlib import Path

from django.core.management.base import BaseCommand

ROOT = Path(__file__).resolve().parents[3]
MODES = {"team": "tu carrito", "ai": "el carrito de la IA", "solutions": "la solución del docente"}


def run_suite(mode, verbose):
    env = {**os.environ, "SHOP_MODE": mode}
    cmd = [sys.executable, "manage.py", "test", "shop", "-v", "2" if verbose else "1"]
    proc = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True, text=True, encoding="utf-8")
    out = proc.stdout + proc.stderr
    ran = re.search(r"Ran (\d+) tests?", out)
    total = int(ran.group(1)) if ran else 0
    # one entry per test, even if a test with subTest fails several times
    failed = len(set(re.findall(r"^(?:FAIL|ERROR): (\w+) \(", out, flags=re.M)))
    if not ran:  # the suite did not even start (for example, the mode is not available)
        return None, None, out
    return total - failed, failed, out


class Command(BaseCommand):
    help = "Duelo: corre las mismas pruebas contra tu carrito y contra el de la IA, y compara."

    def add_arguments(self, parser):
        parser.add_argument("--modo", choices=sorted(MODES), help="solo un modo, con el detalle de lo que falla")

    def handle(self, *args, **options):
        modes = [options["modo"]] if options["modo"] else ["team", "ai"]
        self.stdout.write("\nDuelo: las mismas pruebas contra cada carrito\n")
        for mode in modes:
            passed, failed, out = run_suite(mode, verbose=bool(options["modo"]))
            if passed is None:
                self.stdout.write(f"{mode:<10} {MODES[mode]:<26} no disponible en esta copia")
                continue
            self.stdout.write(f"{mode:<10} {MODES[mode]:<26} pasan {passed:>3}   fallan {failed:>3}")
            if options["modo"]:
                self.stdout.write(out)
        self.stdout.write("\nPara el detalle de uno: python manage.py duelo --modo ai\n")
