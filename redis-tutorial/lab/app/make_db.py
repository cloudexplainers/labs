# Off camera: the garage's old invoices, 2 million invoice lines in SQLite (garage.db), with no index on part.
import random
import sqlite3

random.seed(169)
PARTS = {"rotors": 89.0, "brake pads": 45.0, "oil filter": 9.5, "wiper blades": 22.0, "spark plugs": 7.0,
         "brake fluid": 14.0, "battery": 160.0, "air filter": 18.0}
db = sqlite3.connect("garage.db")
db.execute("CREATE TABLE invoice_lines (id INTEGER PRIMARY KEY, invoice INTEGER, part TEXT, price REAL)")
names = list(PARTS)
rows = ((i, i // 4, p, round(PARTS[p] * random.uniform(0.85, 1.25), 2))
        for i in range(1, 2_000_001) for p in [random.choice(names)])
db.executemany("INSERT INTO invoice_lines VALUES (?, ?, ?, ?)", rows)
db.commit()
print(db.execute("SELECT COUNT(*) FROM invoice_lines").fetchone()[0])
