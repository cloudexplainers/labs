"""The dispatch board: today's plumbing jobs from the office's MySQL database."""
import configparser
from pathlib import Path

import pymysql

cfg = configparser.ConfigParser()
cfg.read(Path(__file__).with_name("board.ini"))
db = cfg["database"]
try:
    conn = pymysql.connect(host=db["host"], user=db["user"], password=db.get("password", ""),
                           database=db["name"])
except pymysql.err.OperationalError as e:
    raise SystemExit(f"Board can't load today's jobs: {e}")
with conn.cursor() as cur:
    cur.execute("SELECT starts, job, plumber FROM jobs WHERE day = CURDATE() ORDER BY starts")
    rows = cur.fetchall()
print(f"Today's jobs: {len(rows)}")
for starts, job, plumber in rows:
    print(f"  {str(starts)[:-3]:>5}  {job:<32} {plumber}")
