#!/usr/bin/env python3
"""A tiny payment service for P060's lab, standing in for a real provider (Stripe, PayPal, ...).

API keys look like real ones: kp_live_ + 24 letters and digits. Every request is logged with the key it
used and the address it came from, as real providers show in their dashboards. Ana manages her keys with
an account token (her dashboard login), which lives only on her laptop, never in Git.
  GET  /v1/balance, /v1/customers       Authorization: Bearer <api key>
  GET  /admin/keys, /admin/log?key=ID   X-Account-Token: <token>
  POST /admin/keys/<id>/roll            revoke that key now, return a new one
"""
import json
import secrets
import string
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

STATE = "/srv/pay/state.json"
ALNUM = string.ascii_letters + string.digits
CUSTOMERS = [
    {"name": "Maya Chen", "email": "maya@example.com", "card": "visa ...4242"},
    {"name": "Omar Haddad", "email": "omar@example.org", "card": "mastercard ...4444"},
    {"name": "Lena Novak", "email": "lena@example.net", "card": "visa ...1881"},
]


def load():
    with open(STATE) as f:
        return json.load(f)


def save(s):
    with open(STATE, "w") as f:
        json.dump(s, f, indent=1)


def new_key():
    return {"id": "key_" + secrets.token_hex(2), "secret": "kp_live_" + "".join(secrets.choice(ALNUM) for _ in range(24)),
            "created": time.strftime("%H:%M"), "revoked": None, "last_used": None, "last_from": None}


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def reply(self, code, body):
        data = json.dumps(body, indent=2).encode() + b"\n"
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def api(self, s, path):
        auth = self.headers.get("Authorization", "")
        secret = auth.removeprefix("Bearer ").strip()
        key = next((k for k in s["keys"] if k["secret"] == secret), None)
        if not key:
            code, body = 401, {"error": "invalid API key"}
        elif key["revoked"]:
            code, body = 401, {"error": "API key revoked"}
        elif path == "/v1/balance":
            code, body = 200, {"available": "1,284.50 USD"}
        elif path == "/v1/customers":
            code, body = 200, {"data": CUSTOMERS}
        else:
            code, body = 404, {"error": "not found"}
        if key:
            s["log"].append({"time": time.strftime("%H:%M:%S"), "from": self.client_address[0], "key": key["id"],
                             "request": f"{self.command} {path}", "status": code})
            if code == 200:
                key["last_used"], key["last_from"] = time.strftime("%H:%M"), self.client_address[0]
        save(s)
        self.reply(code, body)

    def admin(self, s, path, q):
        if self.headers.get("X-Account-Token") != s["account_token"]:
            return self.reply(403, {"error": "not signed in"})
        if path == "/admin/keys" and self.command == "GET":
            return self.reply(200, {"keys": [{k: v for k, v in key.items() if k != "secret"} | {"hint": key["secret"][-4:]}
                                             for key in s["keys"]]})
        if path == "/admin/log":
            return self.reply(200, {"log": [e for e in s["log"] if e["key"] == q.get("key", [""])[0]]})
        parts = path.split("/")
        if self.command == "POST" and len(parts) == 5 and parts[4] == "roll":
            old = next((k for k in s["keys"] if k["id"] == parts[3] and not k["revoked"]), None)
            if not old:
                return self.reply(404, {"error": "no such active key"})
            old["revoked"] = time.strftime("%H:%M")
            k = new_key()
            s["keys"].append(k)
            save(s)
            return self.reply(200, {"revoked": old["id"], "new": {"id": k["id"], "secret": k["secret"]}})
        self.reply(404, {"error": "not found"})

    def handle_one(self):
        s = load()
        u = urlparse(self.path)
        if u.path.startswith("/admin/"):
            self.admin(s, u.path, parse_qs(u.query))
        else:
            self.api(s, u.path)

    do_GET = do_POST = handle_one


if __name__ == "__main__":
    if sys.argv[1:] == ["init"]:
        save({"account_token": secrets.token_hex(16), "keys": [new_key()], "log": []})
    else:
        ThreadingHTTPServer(("0.0.0.0", 80), H).serve_forever()
