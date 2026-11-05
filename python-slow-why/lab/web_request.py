"""One web request to Ana's shop: how long Python runs vs how long it waits for the database."""
import json, sqlite3, time
db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE orders (id INTEGER, item TEXT, total REAL)")
db.executemany("INSERT INTO orders VALUES (?, ?, ?)", [(i, "house blend", 12.5) for i in range(20)])
DB_WAIT = 0.050                              # a typical database / network round trip: 50 ms
def handle():
    t0 = time.perf_counter()
    time.sleep(DB_WAIT)                      # waiting for the database server to answer
    t1 = time.perf_counter()
    rows = db.execute("SELECT id, item, total FROM orders").fetchall()
    body = json.dumps([{"id": r[0], "item": r[1], "total": r[2]} for r in rows])
    t2 = time.perf_counter()
    return t1 - t0, t2 - t1
waits, runs = zip(*[handle() for _ in range(20)])
wait, run = sorted(waits)[10], sorted(runs)[10]
print(f"waiting for the database: {wait * 1000:.1f} ms")
print(f"python code running:      {run * 1000:.2f} ms")
print(f"share of time in python:  {run / (wait + run):.1%}")
