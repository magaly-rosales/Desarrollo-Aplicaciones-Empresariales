import urllib.request, json

url = 'http://127.0.0.1:8000/api/questions/'
body = {"exam": 1, "text": "Pregunta Postman test", "choices": [{"text": "Opcion A", "is_correct": True}, {"text": "Opcion B", "is_correct": False}]}
data = json.dumps(body).encode('utf-8')

req = urllib.request.Request(url, data=data, method='POST')
req.add_header('Authorization', 'Token 0dbf72f7b499c9fc62acc6fd674a95ddb4e52641')
req.add_header('Accept', 'application/json')
req.add_header('Content-Type', 'application/json')

try:
    resp = urllib.request.urlopen(req)
    print(f'Status: {resp.status}')
    print(resp.read().decode()[:500])
except urllib.error.HTTPError as e:
    print(f'Status: {e.code}')
    print(e.read().decode()[:3000])
