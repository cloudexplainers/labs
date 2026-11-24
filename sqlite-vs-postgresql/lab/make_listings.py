"""Off screen: the office's 2,000 listings, the same rows in listings.db (SQLite) and the listings database
(PostgreSQL). Made-up streets and prices; a fixed seed so every run is the same."""
import random
import sqlite3

import psycopg2

random.seed(107)
STREETS = ["Elm St", "Oak Ave", "Maple Dr", "Cedar Ln", "Birch Rd", "Pine St", "Willow Way", "Lake Rd", "Hill St",
           "Park Ave", "River Rd", "Mill Ln", "Orchard Dr", "Church St", "Spring St", "Ridge Rd"]
rows = []
for i in range(2000):
    street = random.choice(STREETS)
    num = random.randint(2, 980)
    if (num, street) == (12, "Elm St"):
        num = 14
    rows.append((f"{num} {street}", random.randrange(189_000, 1_250_000, 500), random.randint(1, 5)))

lite = sqlite3.connect("/home/joe/site/listings.db")
lite.execute("CREATE TABLE listings (id INTEGER PRIMARY KEY, address TEXT NOT NULL, price INTEGER, beds INTEGER)")
lite.executemany("INSERT INTO listings (address, price, beds) VALUES (?, ?, ?)", rows)
lite.commit()

pg = psycopg2.connect(dbname="listings")
cur = pg.cursor()
cur.execute("CREATE TABLE listings (id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY, address text NOT NULL, "
            "price integer, beds integer)")
cur.executemany("INSERT INTO listings (address, price, beds) VALUES (%s, %s, %s)", rows)
cur.execute("GRANT SELECT, INSERT ON listings TO jess")
pg.commit()
print(len(rows))
