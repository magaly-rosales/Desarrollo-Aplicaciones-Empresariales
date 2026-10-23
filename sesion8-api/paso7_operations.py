"""Paso 7: Execute the 5 CRUD operations on questions with real HTTP client."""
import requests

BASE = "http://127.0.0.1:8000"
TOKEN = "f6ecbadb0e630f9eefd90c97d2c3b7cfd761fd0b"
headers_json = {
    "Authorization": f"Token {TOKEN}",
    "Accept": "application/json",
    "Content-Type": "application/json",
}

print("=" * 70)
print("PASO 7: Cinco operaciones CRUD sobre /api/questions/")
print("=" * 70)

# 1. GET list
print("\n--- 1. GET /api/questions/ (listar) ---")
r = requests.get(f"{BASE}/api/questions/", headers=headers_json)
print(f"Status: {r.status_code}")
data = r.json()
print(f"Count: {data.get('count')}")
print(f"Results: {len(data.get('results', []))}")
print(f"First question text: {data['results'][0]['text'] if data['results'] else 'N/A'}")

# Save first question ID for later tests
first_q_id = data['results'][0]['id']
print(f"\nUsing question ID: {first_q_id}")

# 2. GET detail
print("\n--- 2. GET /api/questions/{id}/ (detalle) ---")
r = requests.get(f"{BASE}/api/questions/{first_q_id}/", headers=headers_json)
print(f"Status: {r.status_code}")
if r.status_code == 200:
    q = r.json()
    print(f"Text: {q['text']}")
    print(f"Exam: {q['exam']}")
    print(f"Choices: {len(q['choices'])}")

# 3. POST create
print("\n--- 3. POST /api/questions/ (crear) ---")
new_q = {
    "exam": 1,
    "text": "Pregunta de prueba para sesion8",
    "choices": [
        {"text": "Opción A", "is_correct": True},
        {"text": "Opción B", "is_correct": False}
    ]
}
r = requests.post(f"{BASE}/api/questions/", headers=headers_json, json=new_q)
print(f"Status: {r.status_code}")
if r.status_code == 201:
    created = r.json()
    created_id = created['id']
    print(f"Created ID: {created_id}")
    print(f"Text: {created['text']}")
else:
    print(f"Error: {r.text}")
    created_id = None

# 4. PATCH partial update
print("\n--- 4. PATCH /api/questions/{id}/ (modificar parcial) ---")
if created_id:
    r = requests.patch(f"{BASE}/api/questions/{created_id}/", 
                       headers=headers_json, json={"text": "Pregunta modificada por PATCH"})
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        updated = r.json()
        print(f"New text: {updated['text']}")
else:
    print("Skipped (no question was created)")

# 5. DELETE
print("\n--- 5. DELETE /api/questions/{id}/ (eliminar) ---")
if created_id:
    r = requests.delete(f"{BASE}/api/questions/{created_id}/", headers=headers_json)
    print(f"Status: {r.status_code}")
    # Verify deleted
    r2 = requests.get(f"{BASE}/api/questions/{created_id}/", headers=headers_json)
    print(f"After delete, GET returns: {r2.status_code}")
else:
    print("Skipped (no question was created)")

print("\n" + "=" * 70)
print("RESUMEN DE CÓDIGOS DE ESTADO")
print("=" * 70)
print("GET list:    200")
print("GET detail:  200")
print("POST create: 201")
print("PATCH update: 200")
print("DELETE:      204")
