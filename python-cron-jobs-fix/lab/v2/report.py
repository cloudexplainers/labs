import csv
import os
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent

with open(HERE / "rentals.csv") as f:
    rows = list(csv.DictReader(f))

total = sum(float(r["paid"]) for r in rows)
key = os.environ["BIKES_API_KEY"]

reply = requests.post(
    "http://localhost:8000/daily",
    json={"sender": "report.py", "rentals": len(rows), "takings": total},
    headers={"X-API-Key": key},
    timeout=10,
)
reply.raise_for_status()
print(f"Report sent: {len(rows)} rentals, ${total:.2f}")
