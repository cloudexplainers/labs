"""Ana's tea shop: a tiny web app that keeps its orders in PostgreSQL.

GET /        -> how many orders the database holds
POST /order  -> adds one order
It connects to the database once, at start, at the host named in DB_HOST.
"""
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

import psycopg

NAME = os.environ.get("SHOP_NAME", "Ana's tea shop")
db = psycopg.connect(host=os.environ["DB_HOST"], user="postgres", password=os.environ["DB_PASSWORD"],
                     autocommit=True)
db.execute("CREATE TABLE IF NOT EXISTS orders (id serial PRIMARY KEY, tea text NOT NULL)")
print("connected to the database at", os.environ["DB_HOST"], flush=True)


class Shop(BaseHTTPRequestHandler):
    def reply(self, text):
        body = (text + "\n").encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        n = db.execute("SELECT count(*) FROM orders").fetchone()[0]
        self.reply(f"{NAME}: {n} orders")

    def do_POST(self):
        n = db.execute("INSERT INTO orders (tea) VALUES ('sencha') RETURNING id").fetchone()[0]
        self.reply(f"order {n} saved")

    def log_message(self, *args):
        pass


HTTPServer(("", 8000), Shop).serve_forever()
