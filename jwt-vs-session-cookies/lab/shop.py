#!/usr/bin/env python3
"""Ana's kettle shop API (lab only). It logs people in two ways, side by side:

  POST /session/login    a random session id in a cookie; the session itself is stored in Redis
  POST /token/login      a JWT (RS256, 15 minutes), signed with the login server's private key; nothing is stored
  GET  /orders           accepts either: a session cookie (looked up in Redis) or a Bearer token (signature + exp)
  POST /session/logout   deletes the session from Redis
  POST /token/logout     with DENYLIST=on, puts the token's id (jti) on a denylist in Redis until it expires;
                         without it, there is nothing on the server to delete
  GET  /                 a tiny page whose script logs in both ways (for the browser demo)

Settings (environment): SESSION_STORE = redis host or "none" (an empty store of its own), PRIVATE_KEY = path
(only the login server has one), PUBLIC_KEY = path, DENYLIST = on/off.
"""
import json
import os
import secrets
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs

import jwt
import redis

USERS = {"ana": "kettle-2026"}
ORDERS = {"ana": ["#1041 Assam kettle", "#1042 tea strainer", "#1043 green tea"]}
SESSION_SECONDS = 8 * 3600
TOKEN_SECONDS = 15 * 60
STORE_HOST = os.environ.get("SESSION_STORE", "none")
STORE = redis.Redis(host=STORE_HOST, decode_responses=True) if STORE_HOST != "none" else None
PRIVATE = open(os.environ["PRIVATE_KEY"]).read() if os.environ.get("PRIVATE_KEY") else None
PUBLIC = open(os.environ["PUBLIC_KEY"]).read()
DENYLIST = os.environ.get("DENYLIST", "off") == "on"
ISSUER = "https://api1.kettle.test"

PAGE = """<!doctype html><title>Kettle shop</title><p>Kettle shop</p><script>
const form = () => new URLSearchParams({user: "ana", password: "kettle-2026"});
(async () => {
  await fetch("/session/login", {method: "POST", body: form()});
  const r = await (await fetch("/token/login", {method: "POST", body: form()})).json();
  localStorage.setItem("token", r.access_token);
  window.result = "logged in twice: a session cookie, and a token saved in localStorage";
})();
</script>"""


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    server_version = "kettle-shop"
    sys_version = ""

    def log_message(self, fmt, *args):
        pass

    def send(self, code, body, cookie=None, html=False):
        data = (body if html else json.dumps(body) + "\n").encode()
        self.send_response(code)
        if cookie:
            self.send_header("Set-Cookie", cookie)
        self.send_header("Content-Type", "text/html" if html else "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def form(self):
        raw = self.rfile.read(int(self.headers.get("Content-Length", 0))).decode()
        return {k: v[0] for k, v in parse_qs(raw).items()}

    def cookie(self):
        for part in self.headers.get("Cookie", "").split(";"):
            k, _, v = part.strip().partition("=")
            if k == "session" and v:
                return v
        return None

    def bearer(self):
        a = self.headers.get("Authorization", "")
        return a[7:] if a.startswith("Bearer ") else None

    def store(self):
        if STORE is None:
            return {}
        return STORE

    def check_token(self, token):
        try:
            claims = jwt.decode(token, PUBLIC, algorithms=["RS256"], issuer=ISSUER)
        except jwt.ExpiredSignatureError:
            return None, "token expired"
        except jwt.InvalidTokenError as e:
            return None, f"invalid token: {e}"
        if DENYLIST and STORE.exists(f"deny:{claims['jti']}"):
            return None, "token revoked"
        return claims, None

    def do_GET(self):
        if self.path == "/":
            return self.send(200, PAGE, html=True)
        if self.path != "/orders":
            return self.send(404, {"error": "not found"})
        sid, token = self.cookie(), self.bearer()
        if sid:
            raw = self.store().get(f"session:{sid}")
            if not raw:
                return self.send(401, {"error": "no such session"})
            user = json.loads(raw)["user"]
            how = "session found in the store"
        elif token:
            claims, err = self.check_token(token)
            if err:
                return self.send(401, {"error": err})
            user = claims["sub"]
            how = "signature, expiry and denylist checked" if DENYLIST else "signature and expiry checked"
        else:
            return self.send(401, {"error": "not logged in"})
        self.send(200, {"user": user, "orders": len(ORDERS[user]), "checked": how})

    def do_POST(self):
        if self.path in ("/session/login", "/token/login"):
            f = self.form()
            if USERS.get(f.get("user")) != f.get("password"):
                return self.send(401, {"error": "wrong user or password"})
            if PRIVATE is None:
                return self.send(403, {"error": "this server can't sign anything"})
            user = f["user"]
            if self.path == "/session/login":
                sid = secrets.token_urlsafe(32)
                STORE.set(f"session:{sid}", json.dumps({"user": user, "created": int(time.time())}),
                          ex=SESSION_SECONDS)
                return self.send(200, {"message": f"logged in as {user}"},
                                 cookie=f"session={sid}; Domain=kettle.test; Path=/; Max-Age={SESSION_SECONDS}; "
                                        "HttpOnly; SameSite=Lax")
            now = int(time.time())
            claims = {"iss": ISSUER, "sub": user, "iat": now, "exp": now + TOKEN_SECONDS, "jti": uuid.uuid4().hex}
            token = jwt.encode(claims, PRIVATE, algorithm="RS256")
            return self.send(200, {"access_token": token, "expires_in": TOKEN_SECONDS})
        if self.path == "/session/logout":
            sid = self.cookie()
            if sid:
                self.store().delete(f"session:{sid}")
            return self.send(200, {"message": "logged out"},
                             cookie="session=; Domain=kettle.test; Path=/; Max-Age=0; HttpOnly; SameSite=Lax")
        if self.path == "/token/logout":
            token = self.bearer()
            if DENYLIST and token:
                claims, err = self.check_token(token)
                if claims:
                    left = claims["exp"] - int(time.time())
                    STORE.set(f"deny:{claims['jti']}", claims["sub"], ex=max(left, 1))
            return self.send(200, {"message": "logged out"})
        self.send(404, {"error": "not found"})


if __name__ == "__main__":
    print(f"listening: store={STORE_HOST} signs={'yes' if PRIVATE else 'no'} denylist={DENYLIST}", flush=True)
    ThreadingHTTPServer(("0.0.0.0", 80), Handler).serve_forever()
