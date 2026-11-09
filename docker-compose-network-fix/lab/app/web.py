"""Ana's tea shop: lists the teas from PostgreSQL on port 8000.

It connects to the database once when it starts, and stops if it can't (like most web apps)."""
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

import psycopg

DB = dict(host=os.environ["DB_HOST"], port=os.environ.get("DB_PORT", "5432"),
          user="postgres", password=os.environ["DB_PASSWORD"], dbname="postgres", connect_timeout=5)

print(f"web: connecting to the database at {DB['host']}:{DB['port']}")
try:
    psycopg.connect(**DB).close()
except psycopg.OperationalError as e:
    print(f"web: {str(e).splitlines()[0]}")  # the library's first line
    sys.exit(1)
print("web: connected, serving the shop on port 8000")


class Shop(BaseHTTPRequestHandler):
    def do_GET(self):
        with psycopg.connect(**DB) as db:
            teas = db.execute("SELECT name, price FROM teas ORDER BY name").fetchall()
        body = "".join(f"{name}: ${price}\n" for name, price in teas)
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(body.encode())

    def log_message(self, *args):
        pass


HTTPServer(("0.0.0.0", 8000), Shop).serve_forever()
