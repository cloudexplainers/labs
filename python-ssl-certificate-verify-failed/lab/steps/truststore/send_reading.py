import truststore
truststore.inject_into_ssl()
import requests

URL = "https://portal.coop.lan/api/readings"
reading = {"tank": 1, "celsius": 3.4}

r = requests.post(URL, json=reading, timeout=10)
print("Reading sent:", r.json())
