import json
import os
import re
import subprocess
import sys

from django.core.management.base import BaseCommand

from shop import gate
from shop.management.commands.duelo import MODES, ROOT, run_suite


def failing_tests(out):
    """Dotted names of the tests that failed or raised, without repetitions."""
    return sorted(set(re.findall(r"^(?:FAIL|ERROR): \w+ \(([^)]+)\)", out, flags=re.M)))


def replay_audit(mode, paths):
    """Run audit_cart --replay --json with the fixed catalog for one mode; None if it cannot run."""
    env = {**os.environ, "SHOP_MODE": mode}
    cmd = [sys.executable, "manage.py", "audit_cart", *paths, "--replay", "--json", "--catalogo-fijo"]
    proc = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True, text=True, encoding="utf-8")
    if proc.returncode != 0:
        return None
    try:
        return json.loads(proc.stdout)["carts"]
    except (ValueError, KeyError):
        return None


class Command(BaseCommand):
    help = ("Compuerta sin pantalla para un cambio del agente: corre las pruebas y la auditoría con replay "
            "contra una implementación y decide aceptar (código 0), rechazar (1) o no disponible (2).")

    def add_arguments(self, parser):
        parser.add_argument("paths", nargs="*", help="carritos a reproducir (por defecto, carts/*.json)")
        parser.add_argument("--modo", choices=sorted(MODES),
                            help="implementación a juzgar (por defecto, la de SHOP_MODE o team)")
        parser.add_argument("--json", action="store_true", help="salida en JSON, para un agente o un script")

    def handle(self, *args, **options):
        mode = options["modo"] or os.environ.get("SHOP_MODE", "team")
        paths = options["paths"] or sorted(str(p.relative_to(ROOT)) for p in (ROOT / "carts").glob("*.json"))

        passed, failed, out = run_suite(mode, verbose=False)
        tests = {"total": 0, "passed": 0, "failed": 0, "failing": []}
        carts = []
        if passed is not None:
            tests = {"total": passed + failed, "passed": passed, "failed": failed, "failing": failing_tests(out)}
            report = replay_audit(mode, paths)
            if report is None:
                tests["total"] = 0  # the audit could not run: nothing to judge
            else:
                for entry in report:
                    expected, result = gate.judge_cart(entry["findings"])
                    carts.append({"file": entry["file"], "expected": expected, "result": result})
        verdict, code = gate.verdict(tests["total"], tests["failed"], carts)

        if options["json"]:
            self.stdout.write(json.dumps({"mode": mode, "tests": tests, "carts": carts,
                                          "verdict": verdict, "exit_code": code}, ensure_ascii=False, indent=2))
        else:
            self.stdout.write(f"\nCompuerta: {MODES[mode]} (modo {mode})\n")
            if verdict == "no_disponible":
                self.stdout.write("  no se pudo juzgar: el modo no existe en esta copia o falta el catálogo\n")
            else:
                self.stdout.write(f"  pruebas     pasan {tests['passed']:>3}   fallan {tests['failed']:>3}")
                for name in tests["failing"][:8]:
                    self.stdout.write(f"              {name}")
                if len(tests["failing"]) > 8:
                    self.stdout.write(f"              … y {len(tests['failing']) - 8} más")
                ok = sum(1 for c in carts if c["result"] == "ok")
                self.stdout.write(f"  carritos    {ok} de {len(carts)} como se esperaba")
                for c in carts:
                    if c["result"] != "ok":
                        self.stdout.write(f"              {c['file']}: {gate.RESULTS[c['result']]} (se esperaba: {c['expected']})")
            self.stdout.write(f"  veredicto   {verdict.upper().replace('_', ' ')} (código de salida {code})\n")
        sys.exit(code)
