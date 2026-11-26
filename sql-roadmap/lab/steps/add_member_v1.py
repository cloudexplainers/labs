import sys
import psycopg2

name = sys.argv[1]
conn = psycopg2.connect(dbname="club")
cur = conn.cursor()
cur.execute(f"INSERT INTO members (name) VALUES ('{name}')")
conn.commit()
print("Added", name)
