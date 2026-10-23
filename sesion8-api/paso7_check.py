"""Paso 7: Check if API is navigable, then apply minimal change if needed, and test 5 operations."""
import subprocess
import sys
import requests
import time
import signal
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

HUMAN_TOKEN = "f6ecbadb0e630f9eefd90c97d2c3b7cfd761fd0b"
BASE = "http://127.0.0.1:8000"
headers = {
    "Authorization": f"Token {HUMAN_TOKEN}",
    "Accept": "application/json",
}

print("=" * 60)
print("PASO 7: API Navegable - Verificación inicial")
print("=" * 60)

# Test 1: Try to access API without token (browser-like request)
print("\n--- Test: GET /api/ sin token (como navegador) ---")
r = requests.get(f"{BASE}/api/")
print(f"Status: {r.status_code}")
print(f"Response (first 500 chars): {r.text[:500]}")

# Test 2: Try with token
print("\n--- Test: GET /api/ con token ---")
r = requests.get(f"{BASE}/api/", headers=headers)
print(f"Status: {r.status_code}")
print(f"Response (first 500 chars): {r.text[:500]}")
