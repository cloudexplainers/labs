import sqlite3
import time

import redis

r = redis.Redis(decode_responses=True)
db = sqlite3.connect("garage.db")


def average_price(part):
    key = f"price:{part}"
    cached = r.get(key)
    if cached is not None:
        return float(cached), "Redis"
    sql = "SELECT AVG(price) FROM invoice_lines WHERE part = ?"
    price = db.execute(sql, (part,)).fetchone()[0]
    r.set(key, price, ex=600)
    return price, "the database"


for _ in range(2):
    start = time.perf_counter()
    price, source = average_price("rotors")
    ms = (time.perf_counter() - start) * 1000
    print(f"rotors: ${price:.2f} from {source} in {ms:.1f} ms")
