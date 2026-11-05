import random
import sqlite3
import time

db = sqlite3.connect("orders.db")
db.execute("CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, tea TEXT, grams INTEGER)")
if db.execute("SELECT count(*) FROM orders").fetchone()[0] == 0:
    with db:
        db.executemany("INSERT INTO orders VALUES (?, ?, ?)",
                       ((i, random.choice(["Sencha", "Earl Grey", "Oolong"]), random.randint(50, 500))
                        for i in range(1, 100_001)))
ids = [random.randint(1, 100_000) for _ in range(100_000)]
start = time.perf_counter()
for i in ids:
    db.execute("SELECT tea, grams FROM orders WHERE id = ?", (i,)).fetchone()
took = time.perf_counter() - start
print(f"100,000 lookups in {took:.2f} seconds")
print(f"{took / 100_000 * 1e6:.1f} microseconds each")
