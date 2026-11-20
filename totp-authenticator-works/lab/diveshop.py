"""The dive shop's booking site: a password, then a six-digit code from an authenticator app (TOTP, RFC 6238).

GET  /setup/<user>          turn on two-step login: a new secret, shown as a QR code (an otpauth:// link) and as text
GET  /setup/<user>/qr.png   the same QR code as a picture
POST /login                 user, password, code -> plain text

Codes are checked with pyotp for the current 30-second time step and one step either side (clocks drift a little),
each time step's code works once, and five wrong codes in a row lock the account for five minutes.
"""
import base64
import hmac
import json
import subprocess
import logging
import time
from pathlib import Path

import pyotp
from flask import Flask, Response, request
from werkzeug.security import check_password_hash, generate_password_hash

DB = Path("/var/lib/diveshop/users.json")
ISSUER = "Dive Shop"
LOCK_AFTER, LOCK_SECONDS = 5, 300
app = Flask(__name__)
logging.getLogger("werkzeug").setLevel(logging.ERROR)   # keep the journal to login results


def load():
    if not DB.exists():
        DB.write_text(json.dumps({"ana": {"password": generate_password_hash("coral-reef-9")}}, indent=1))
    return json.loads(DB.read_text())


def save(users):
    DB.write_text(json.dumps(users, indent=1) + "\n")


def say(text, status=200):
    return Response(text + "\n", status=status, mimetype="text/plain")


def qr_png(uri):
    return subprocess.run(["qrencode", "-o", "-", "-s", "8", "-m", "2", uri], capture_output=True, check=True).stdout


@app.get("/setup/<user>")
def setup(user):
    users = load()
    secret = pyotp.random_base32()
    users[user]["totp_secret"] = secret
    users[user].pop("last_step", None)
    save(users)
    uri = pyotp.TOTP(secret).provisioning_uri(name=user, issuer_name=ISSUER)
    print(f"setup {user}: new secret saved", flush=True)
    img = base64.b64encode(qr_png(uri)).decode()
    spaced = " ".join(secret[i:i + 4] for i in range(0, len(secret), 4))
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>Two-step login - Dive Shop</title>
<style>body{{font-family:system-ui,sans-serif;background:#eef6f8;color:#123;margin:0}}
header{{background:#0b5e7a;color:#fff;padding:18px 40px;font-size:26px;font-weight:700}}
main{{display:flex;gap:56px;padding:36px 40px;align-items:flex-start}}
h1{{margin:0 0 12px;font-size:30px}} p{{font-size:20px;line-height:1.5;margin:0 0 14px;max-width:640px}}
#qr{{background:#fff;padding:12px;border-radius:10px;box-shadow:0 2px 10px #0002}}
#secret{{font-family:ui-monospace,monospace;font-size:24px;background:#fff;padding:10px 14px;border-radius:8px;
letter-spacing:1px;display:inline-block}}</style></head>
<body><header>Dive Shop &middot; booking</header><main>
<img id="qr" src="data:image/png;base64,{img}" alt="QR code" width="300" height="300">
<div><h1>Turn on two-step login</h1>
<p>Scan this code with your authenticator app. From now on, you sign in with your password and the six-digit code
the app shows.</p>
<p>Can't scan it? Type this key into the app instead:</p>
<div id="secret">{spaced}</div></div></main></body></html>"""


@app.get("/setup/<user>/qr.png")
def setup_qr(user):
    secret = load()[user]["totp_secret"]
    uri = pyotp.TOTP(secret).provisioning_uri(name=user, issuer_name=ISSUER)
    return Response(qr_png(uri), mimetype="image/png")


@app.post("/login")
def login():
    user, password, code = (request.form.get(k, "") for k in ("user", "password", "code"))
    users = load()
    u = users.get(user)
    if not u or not check_password_hash(u["password"], password):
        return say("Wrong user name or password.", 401)
    now = time.time()
    if u.get("locked_until", 0) > now:
        wait = int(u["locked_until"] - now + 59) // 60
        print(f"login {user}: locked, code not checked", flush=True)
        return say(f"Too many wrong codes. Try again in {wait} minutes.", 429)
    totp, step = pyotp.TOTP(u["totp_secret"]), int(now // 30)
    match = next((s for s in (step, step - 1, step + 1) if hmac.compare_digest(totp.at(s * 30), code)), None)
    if match is None:
        u["fails"] = u.get("fails", 0) + 1
        if u["fails"] >= LOCK_AFTER:
            u["locked_until"], u["fails"] = now + LOCK_SECONDS, 0
        save(users)
        print(f"login {user}: code {code} matches no time step near {step}", flush=True)
        return say("Wrong code.", 401)
    if match <= u.get("last_step", -1):
        print(f"login {user}: code {code} (time step {match}) was already used", flush=True)
        return say("That code was already used. Wait for the next one.", 401)
    u["last_step"], u["fails"] = match, 0
    save(users)
    print(f"login {user}: code {code} matches time step {match} (now {step})", flush=True)
    return say(f"Welcome back, {user.capitalize()}. You're signed in.")
