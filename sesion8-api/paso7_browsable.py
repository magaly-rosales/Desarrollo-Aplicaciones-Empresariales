"""Paso 7: Verify browsable API works with the minimal change applied."""
import requests

BASE = "http://127.0.0.1:8000"
TOKEN = "f6ecbadb0e630f9eefd90c97d2c3b7cfd761fd0b"
headers_json = {
    "Authorization": f"Token {TOKEN}",
    "Accept": "text/html",
}

print("=" * 70)
print("PASO 7: Verificación API Navegable (HTML)")
print("=" * 70)

# Check if browsable API returns HTML
print("\n--- GET /api/ con Accept: text/html ---")
r = requests.get(f"{BASE}/api/", headers=headers_json)
print(f"Status: {r.status_code}")
print(f"Content-Type: {r.headers.get('Content-Type')}")
print(f"Response (first 800 chars):\n{r.text[:800]}")

print("\n--- GET /api/questions/ con Accept: text/html ---")
r = requests.get(f"{BASE}/api/questions/", headers=headers_json)
print(f"Status: {r.status_code}")
print(f"Content-Type: {r.headers.get('Content-Type')}")
print(f"Response (first 800 chars):\n{r.text[:800]}")
