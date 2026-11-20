"""The city marathon's sign-up app (P113). One copy runs on each web server; the server's name is in every answer.

Entries in a runner's basket live in this process's memory, keyed by a cookie, the way many small apps start out (one gunicorn process, so one memory):
that is what a load balancer without sticky sessions breaks. Sign-ups are written to SQLite in /var/lib/signup.
"""
import secrets
import socket
import sqlite3

from flask import Flask, request, make_response

app = Flask(__name__)
NAME = socket.gethostname()
DB = "/var/lib/signup/signups.db"
BASKETS = {}
PAGE = """<!doctype html><html><head><meta charset="utf-8"><title>City Marathon 2027: sign up</title>
<style>
body{{font-family:system-ui,sans-serif;background:#f6f4ef;color:#1d2433;margin:0}}
header{{background:#1f4e79;color:#fff;padding:28px 48px}} header h1{{margin:0;font-size:40px}}
header p{{margin:6px 0 0;font-size:20px;opacity:.85}}
main{{padding:32px 48px;max-width:900px}}
.races{{display:flex;gap:18px}} .race{{background:#fff;border:1px solid #d9d4c7;border-radius:10px;padding:18px 22px;flex:1}}
.race h2{{margin:0 0 6px;font-size:26px}} .race p{{margin:0;color:#5b6475;font-size:18px}}
#basket{{margin-top:28px;background:#fff;border:2px solid #1f4e79;border-radius:10px;padding:18px 22px;font-size:22px}}
#basket h2{{margin:0 0 8px;font-size:24px}}
footer{{padding:0 48px 32px;color:#5b6475;font-size:18px}} #server{{font-weight:700;color:#1d2433}}
</style></head><body>
<header><h1>City Marathon 2027</h1><p>Sign-ups are open. Pick your race.</p></header>
<main><div class="races">
<div class="race"><h2>10K</h2><p>Sunday 9 May, 8:00</p></div>
<div class="race"><h2>Half marathon</h2><p>Sunday 9 May, 7:30</p></div>
<div class="race"><h2>Marathon</h2><p>Sunday 9 May, 7:00</p></div>
</div>
<div id="basket"><h2>Your basket</h2>{basket}</div></main>
<footer>Page served by <span id="server">{name}</span></footer></body></html>"""


def basket_id():
    return request.cookies.get("basket")


@app.get("/")
def home():
    items = BASKETS.get(basket_id(), [])
    basket = ", ".join(items) if items else "Your basket is empty."
    return PAGE.format(basket=basket, name=NAME)


@app.get("/hello")
def hello():
    return f"Hello from {NAME}\n"


@app.get("/add")
def add():
    bid = basket_id() or secrets.token_hex(8)
    race = request.args.get("race", "10K")
    BASKETS.setdefault(bid, []).append(race)
    resp = make_response(f"{NAME}: added {race}\n")
    resp.set_cookie("basket", bid)
    return resp


@app.get("/basket")
def basket():
    items = BASKETS.get(basket_id(), [])
    return f"{NAME}: " + (", ".join(items) if items else "basket empty") + "\n"


@app.post("/signup")
def signup():
    name = request.form.get("name", "runner")
    try:
        with sqlite3.connect(DB) as db:
            db.execute("CREATE TABLE IF NOT EXISTS runners (name TEXT)")
            n = db.execute("INSERT INTO runners VALUES (?)", (name,)).lastrowid
    except sqlite3.Error as e:
        return f"{NAME}: 500 sign-up failed: {e}\n", 500
    return f"{NAME}: thanks {name}, you're signed up\n"


@app.get("/health")
def health():
    """Can this server really take a sign-up? Write to its database and roll back."""
    try:
        with sqlite3.connect(DB) as db:
            db.execute("CREATE TABLE IF NOT EXISTS health (t TEXT)")
            db.execute("INSERT INTO health VALUES ('x')")
            db.rollback()
    except sqlite3.Error as e:
        return f"{NAME}: {e}\n", 500
    return f"{NAME}: ok\n"
