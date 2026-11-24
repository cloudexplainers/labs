"""Looks up 10,000 listings by id, one query each, the way a busy page would: SQLite vs PostgreSQL on this server."""
import random
import sqlite3
import time

import psycopg2

ids = [random.randint(1, 2000) for _ in range(10_000)]

lite = sqlite3.connect("listings.db")
t = time.perf_counter()
for i in ids:
    lite.execute("SELECT address, price FROM listings WHERE id = ?", (i,)).fetchone()
print(f"SQLite:     10,000 lookups in {time.perf_counter() - t:.3f} s")

pg = psycopg2.connect(dbname="listings")
cur = pg.cursor()
t = time.perf_counter()
for i in ids:
    cur.execute("SELECT address, price FROM listings WHERE id = %s", (i,))
    cur.fetchone()
print(f"PostgreSQL: 10,000 lookups in {time.perf_counter() - t:.3f} s")
