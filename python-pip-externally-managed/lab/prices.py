import requests

r = requests.get("http://localhost:8000/prices.json", timeout=5)
for tea, price in r.json().items():
    print(f"{tea:<12} ${price:.2f}")
