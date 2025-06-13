import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def print_response(resp):
    print(f"Status Code: {resp.status_code}")
    try:
        print("Response:", json.dumps(resp.json(), indent=2))
    except Exception:
        print("Response (raw):", resp.text)

# 1. Sprawdź cały łańcuch bloków
print("\n[1] GET /chain")
response = requests.get(f"{BASE_URL}/chain")
print_response(response)

# 2. Dodaj transakcję
print("\n[2] POST /transactions/new")
transaction_data = {
    "sender": "Alice",
    "recipient": "Bob",
    "amount": 25
}
response = requests.post(f"{BASE_URL}/transactions/new", json=transaction_data)
print_response(response)

# 3. Wydobądź nowy blok
print("\n[3] GET /mine")
response = requests.get(f"{BASE_URL}/mine")
print_response(response)

# 4. Sprawdź cały łańcuch ponownie
print("\n[4] GET /chain (after mining)")
response = requests.get(f"{BASE_URL}/chain")
print_response(response)
