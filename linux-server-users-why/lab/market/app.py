"""Riverside farmers market: the order-ahead app (Flask, run by gunicorn behind nginx)."""
import json
import sqlite3
import threading
import urllib.request

from flask import Flask, jsonify, request

app = Flask(__name__)
DB = "file:/srv/market/market.db?mode=ro"
local = threading.local()


def db():
    if not hasattr(local, "conn"):
        local.conn = sqlite3.connect(DB, uri=True, check_same_thread=False)
    return local.conn


@app.get("/api/stalls")
def stalls():
    rows = db().execute("SELECT id, name, stall, price FROM products ORDER BY id").fetchall()
    return jsonify([{"id": r[0], "name": r[1], "stall": r[2], "price": r[3]} for r in rows])


@app.get("/api/orders")
def orders():
    rows = db().execute("SELECT id, day, total FROM orders WHERE customer_id = ? ORDER BY id DESC LIMIT 10",
                        (int(request.args["customer"]),)).fetchall()
    return jsonify([{"id": r[0], "day": r[1], "total": r[2]} for r in rows])


@app.post("/api/checkout")
def checkout():
    # The card payment service answers in about 200 ms, like a real card processor.
    with urllib.request.urlopen("http://payments:9000/charge", data=b"{}", timeout=10) as r:
        return jsonify(json.loads(r.read()))
