import requests
import json

url = "http://127.0.0.1:8080/generate_quote"
payload = {
    "client_name": "TestClient",
    "items": [{"model": "iPhone 13", "capacity": "128GB", "price": "15000"}]
}
headers = {"Content-Type": "application/json"}

try:
    response = requests.post(url, json=payload, headers=headers)
    print(response.text)
except Exception as e:
    print(f"Error: {e}")
