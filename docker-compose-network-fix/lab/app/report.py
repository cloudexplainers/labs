"""Ana's nightly report: how many teas the shop sells and what they're worth."""
import os
import sys

import psycopg

try:
    with psycopg.connect(host=os.environ["DB_HOST"], port=os.environ.get("DB_PORT", "5432"), user="postgres",
                         password=os.environ["DB_PASSWORD"], dbname="postgres", connect_timeout=5) as db:
        count, total = db.execute("SELECT count(*), sum(price) FROM teas").fetchone()
except psycopg.OperationalError as e:
    print(f"report: {str(e).splitlines()[0]}")
    sys.exit(1)
print(f"report: {count} teas, ${total} for one of each")
