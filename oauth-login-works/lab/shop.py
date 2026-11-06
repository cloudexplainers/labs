#!/usr/bin/env python3
"""Ana's Tea Shop: a tiny web app with a "Sign in with Kettle ID" button.

It follows OAuth 2.0's authorization code flow with PKCE, plus OpenID Connect for the ID token:
  /login     sends the browser to Kettle ID with a state, a nonce and a PKCE challenge
  /callback  Kettle ID sends the browser back here with a one-time code; the shop checks the state,
             swaps the code for tokens (with its client secret and the PKCE verifier), checks the ID token's
             signature, issuer, audience and nonce, then asks Kettle ID's user API who signed in.
The shop never sees Ana's Kettle ID password. Every step goes to /srv/log/shop.log.
"""
import base64
import hashlib
import json
import os
import secrets
import ssl
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import jwt
import requests

ISSUER = "https://id.test/realms/kettle"
OIDC = ISSUER + "/protocol/openid-connect"
CLIENT_ID = "tea-shop"
SECRET = os.environ["CLIENT_SECRET"]
REDIRECT = "https://shop.test/callback"
LOG = "/srv/log/shop.log"
DATA = "/srv/data"
CA = "/etc/ssl/certs/ca-certificates.crt"
sessions = {}


def log(msg):
    with open(LOG, "a") as f:
        f.write(f"{time.strftime('%H:%M:%S')} {msg}\n")


def save(name, obj, mode=0o644):
    path = os.path.join(DATA, name)
    with open(path, "w") as f:
        f.write(obj if isinstance(obj, str) else json.dumps(obj, indent=1))
    os.chmod(path, mode)
    os.chown(path, 1000, 1000)


def b64url(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode()


PAGE = """<!doctype html><html><head><meta charset="utf-8"><title>Ana's Tea Shop</title></head>
<body><h1>{h1}</h1><p>{p}</p></body></html>"""


class Shop(BaseHTTPRequestHandler):
    def send(self, code, h1, p="", headers=()):
        body = PAGE.format(h1=h1, p=p).encode()
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        for k, v in headers:
            self.send_header(k, v)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *a):
        pass

    def sid(self):
        for part in self.headers.get("Cookie", "").split(";"):
            k, _, v = part.strip().partition("=")
            if k == "sid":
                return v
        return None

    def do_GET(self):
        url = urllib.parse.urlparse(self.path)
        q = dict(urllib.parse.parse_qsl(url.query))
        if url.path == "/":
            return self.send(200, "Ana's Tea Shop", '<a id="signin" href="/login">Sign in with Kettle ID</a>')
        if url.path == "/login":
            sid = secrets.token_urlsafe(16)
            state, nonce, verifier = secrets.token_urlsafe(16), secrets.token_urlsafe(16), secrets.token_urlsafe(48)
            challenge = b64url(hashlib.sha256(verifier.encode()).digest())
            sessions[sid] = {"state": state, "nonce": nonce, "verifier": verifier}
            to = OIDC + "/auth?" + urllib.parse.urlencode({
                "response_type": "code", "client_id": CLIENT_ID, "redirect_uri": REDIRECT,
                "scope": "openid profile email", "state": state, "nonce": nonce,
                "code_challenge": challenge, "code_challenge_method": "S256"})
            log(f"login: sent the browser to id.test (state {state[:6]}..., PKCE challenge {challenge[:6]}...)")
            return self.send(302, "Redirecting", headers=[
                ("Location", to), ("Set-Cookie", f"sid={sid}; Path=/; HttpOnly; Secure; SameSite=Lax")])
        if url.path == "/callback":
            s = sessions.pop(self.sid() or "", None)
            if "error" in q:
                log(f"callback: Kettle ID said {q['error']}")
                return self.send(400, "Sign-in cancelled", q["error"])
            if not s or q.get("state") != s["state"]:
                log("callback refused: the state doesn't match a sign-in this browser started")
                return self.send(400, "Sign-in refused", "This sign-in wasn't started here.")
            code = q["code"]
            log(f"callback: state matched; got a one-time code ({code[:6]}...)")
            save("last_code", code, 0o600)
            save("last_verifier", s["verifier"], 0o600)
            r = requests.post(OIDC + "/token", auth=(CLIENT_ID, SECRET), verify=CA, data={
                "grant_type": "authorization_code", "code": code, "redirect_uri": REDIRECT,
                "code_verifier": s["verifier"]})
            if r.status_code != 200:
                log(f"token: Kettle ID answered {r.status_code}: {r.text}")
                return self.send(400, "Sign-in failed", r.text)
            tok = r.json()
            log(f"token: sent the code + client secret + PKCE verifier; got {r.status_code} "
                "with an ID token and an access token")
            idt = tok["id_token"]
            jwks = jwt.PyJWKClient(OIDC + "/certs", ssl_context=ssl.create_default_context(cafile=CA))
            key = jwks.get_signing_key_from_jwt(idt)
            claims = jwt.decode(idt, key.key, algorithms=["RS256"], audience=CLIENT_ID, issuer=ISSUER)
            if claims.get("nonce") != s["nonce"]:
                log("id token refused: nonce doesn't match")
                return self.send(400, "Sign-in refused", "nonce")
            log("id token: signature valid, issuer id.test/realms/kettle, audience tea-shop, nonce matched")
            save("id_token.json", claims)
            save("id_token.raw", idt, 0o600)
            save("tokens.json", tok, 0o600)
            save("access_token", tok["access_token"], 0o600)
            u = requests.get(OIDC + "/userinfo", verify=CA,
                             headers={"Authorization": "Bearer " + tok["access_token"]})
            me = u.json()
            log(f"user API: {u.status_code}, {me.get('name')} <{me.get('email')}> (asked with the access token)")
            return self.send(200, f"Welcome, {me.get('given_name')}", f"Signed in as {me.get('email')}")
        return self.send(404, "Not found")


httpd = ThreadingHTTPServer(("0.0.0.0", 443), Shop)
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.load_cert_chain("/srv/tls/site.crt", "/srv/tls/site.key")
httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)
print("listening on https://shop.test", flush=True)
httpd.serve_forever()
