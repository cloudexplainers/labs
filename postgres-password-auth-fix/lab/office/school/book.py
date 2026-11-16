"""The music school's booking screen: today's lessons, read from the school's database.

The connection address comes from booking.env (DATABASE_URL), as most apps do.
"""
from pathlib import Path

import psycopg2

env = dict(l.split("=", 1) for l in Path(__file__).with_name("booking.env").read_text().split() if "=" in l)
conn = psycopg2.connect(env["DATABASE_URL"])
rows = conn.cursor()
rows.execute("SELECT starts, room, student FROM lessons WHERE day = 'Mon' ORDER BY starts")
for starts, room, student in rows.fetchall():
    print(f"{starts}  room {room}  {student}")
