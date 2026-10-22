"""Paso 1-2: Verify DRF installation and configuration."""
import subprocess
import sys
import json

venv_python = ".venv\\Scripts\\python"

# Check DRF is installed
result = subprocess.run(
    [venv_python, "-c", "import rest_framework; print(rest_framework.VERSION)"],
    capture_output=True, text=True
)
print(f"DRF version: {result.stdout.strip()}")

# Check installed apps
result = subprocess.run(
    [venv_python, "manage.py", "check"],
    capture_output=True, text=True
)
print(f"Django check: {result.stdout.strip()} {result.stderr.strip()}")

# Start server and test endpoints
import requests

# We need to start the server first - use manage.py test instead
result = subprocess.run(
    [venv_python, "manage.py", "test", "quiz.tests.test_api"],
    capture_output=True, text=True
)
print(f"Test API result:\n{result.stdout}")
if result.stderr:
    print(f"stderr: {result.stderr}")
print(f"Return code: {result.returncode}")
