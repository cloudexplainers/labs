import sqlite3
import time

db = sqlite3.connect("shop.db", isolation_level=None)
db.execute("BEGIN")
for name in ["Sencha", "Earl Grey", "Oolong"]:
    db.execute("UPDATE teas SET stock = stock + 100 WHERE name = ?", (name,))
    print(f"restocked {name}", flush=True)
    time.sleep(2)
db.execute("COMMIT")
print("done")
