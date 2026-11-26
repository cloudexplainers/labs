import sys
import psycopg2

name = sys.argv[1]
conn = psycopg2.connect(dbname="club")
cur = conn.cursor()
cur.execute("INSERT INTO members (name) VALUES (%s)", (name,))
conn.commit()
print("Added", name)
