"""Joe's site saves a new listing: python3 add_listing.py sqlite|postgres ADDRESS PRICE"""
import sys

db, address, price = sys.argv[1], sys.argv[2], int(sys.argv[3])
if db == "sqlite":
    import sqlite3
    conn = sqlite3.connect("listings.db")          # Python waits up to 5 seconds for a lock by default
    cur = conn.execute("INSERT INTO listings (address, price) VALUES (?, ?)", (address, price))
    new_id = cur.lastrowid
else:
    import psycopg2
    conn = psycopg2.connect(dbname="listings")
    cur = conn.cursor()
    cur.execute("INSERT INTO listings (address, price) VALUES (%s, %s) RETURNING id", (address, price))
    new_id = cur.fetchone()[0]
conn.commit()
print(f"saved listing {new_id}: {address}")
