"""A tiny HTTPS web site for the P052 lab (Python's own server + py_webauthn).

SITE=shop.test        Ana's Tea Shop: password sign-in (the old way) and passkeys (WebAuthn).
SITE=other-site.test  Any other site: its sign-in page asks the browser for a passkey and shows the answer.
It stores nothing but public keys, and it never sees a private key.
"""
import base64
import hashlib
import json
import os
import ssl
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit

from webauthn import (generate_authentication_options, generate_registration_options, options_to_json,
                      verify_authentication_response, verify_registration_response)
from webauthn.helpers.structs import (AuthenticatorSelectionCriteria, ResidentKeyRequirement,
                                      UserVerificationRequirement)

SITE = os.environ["SITE"]
ORIGIN = f"https://{SITE}"
DATA = "/srv/data/users.json"
challenges = {}     # one-time challenges this site handed out and hasn't seen back yet


def b64(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()


def unb64(s: str) -> bytes:
    return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))


def users() -> dict:
    return json.load(open(DATA)) if os.path.exists(DATA) else {}


def save(u: dict):
    os.makedirs(os.path.dirname(DATA), exist_ok=True)
    json.dump(u, open(DATA, "w"), indent=2)


def log(msg: str):
    line = f"{time.strftime('%H:%M:%S')} {msg}"
    print(line, flush=True)
    os.makedirs("/srv/log", exist_ok=True)
    with open("/srv/log/site.log", "a") as f:
        f.write(line + "\n")


def pw_hash(pw: str, salt: bytes) -> str:
    return b64(hashlib.pbkdf2_hmac("sha256", pw.encode(), salt, 200_000))


PAGE = """<!doctype html><meta charset=utf-8><title>{title}</title>
<h1>{title}</h1><p id=status>working...</p>
<script>
const show = (m) => {{ document.getElementById('status').textContent = m; }};
const dec = (buf) => new TextDecoder().decode(buf);
(async () => {{
  try {{ {body} }}
  catch (e) {{ window.result = {{error: e.name + ': ' + e.message}}; show(window.result.error); }}
}})();
</script>"""

SIGNUP = """
  const o = await (await fetch('/api/register/begin?user=' + new URLSearchParams(location.search).get('user'))).json();
  const c = await navigator.credentials.create({publicKey: PublicKeyCredential.parseCreationOptionsFromJSON(o)});
  const r = await (await fetch('/api/register/finish', {method: 'POST', body: JSON.stringify(c.toJSON())})).json();
  window.result = {message: r.message, clientData: dec(c.response.clientDataJSON)}; show(r.message);"""

SIGNIN = """
  const o = await (await fetch('/api/login/begin')).json();
  const c = await navigator.credentials.get({publicKey: PublicKeyCredential.parseRequestOptionsFromJSON(o)});
  const r = await (await fetch('/api/login/finish', {method: 'POST', body: JSON.stringify(c.toJSON())})).json();
  window.result = {message: r.message, clientData: dec(c.response.clientDataJSON)}; show(r.message);"""

# other-site.test: ask the browser for a passkey, for this site or (?ask=) for another one. Nothing is sent anywhere.
OTHER = """
  const ask = new URLSearchParams(location.search).get('ask') || location.hostname;
  const c = await navigator.credentials.get({publicKey: {challenge: crypto.getRandomValues(new Uint8Array(32)),
                                             rpId: ask, timeout: 8000, userVerification: 'preferred'}});
  window.result = {message: 'got a passkey answer', clientData: dec(c.response.clientDataJSON)}; show(window.result.message);"""


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def send(self, code: int, body, ctype="application/json"):
        data = (json.dumps(body) if ctype == "application/json" else body).encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype + "; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def body(self) -> bytes:
        return self.rfile.read(int(self.headers.get("Content-Length", 0)))

    def page(self, title: str, js: str):
        self.send(200, PAGE.format(title=title, body=js), "text/html")

    def do_GET(self):
        url = urlsplit(self.path)
        q = parse_qs(url.query)
        if SITE != "shop.test":
            if url.path == "/signin":
                return self.page("Other Site: sign in", OTHER)
            return self.send(200, "<h1>Other Site</h1>", "text/html")
        if url.path == "/":
            return self.send(200, "<h1>Ana's Tea Shop</h1>", "text/html")
        if url.path == "/signup":
            return self.page("Ana's Tea Shop: add a passkey", SIGNUP)
        if url.path == "/signin":
            return self.page("Ana's Tea Shop: sign in", SIGNIN)
        if url.path == "/api/register/begin":
            name = q["user"][0]
            u = users()[name]
            opts = generate_registration_options(
                rp_id=SITE, rp_name="Ana's Tea Shop", user_name=name, user_id=unb64(u["id"]),
                authenticator_selection=AuthenticatorSelectionCriteria(
                    resident_key=ResidentKeyRequirement.REQUIRED,
                    user_verification=UserVerificationRequirement.PREFERRED))
            challenges[b64(opts.challenge)] = name
            return self.send(200, json.loads(options_to_json(opts)))
        if url.path == "/api/login/begin":
            opts = generate_authentication_options(rp_id=SITE,
                                                   user_verification=UserVerificationRequirement.PREFERRED)
            challenges[b64(opts.challenge)] = None
            return self.send(200, json.loads(options_to_json(opts)))
        self.send(404, {"message": "not found"})

    def do_POST(self):
        path = urlsplit(self.path).path
        if SITE != "shop.test":
            return self.send(404, {"message": "not found"})
        if path == "/login":                                   # the old way: a password in a form
            f = parse_qs(self.body().decode())
            name, pw = f.get("user", [""])[0], f.get("password", [""])[0]
            u = users().get(name)
            ip = self.client_address[0]
            if u and "pw" in u and pw_hash(pw, unb64(u["salt"])) == u["pw"]:
                log(f"password sign-in OK: {name} from {ip}")
                return self.send(200, f"Welcome back, {name}\n", "text/plain")
            log(f"password sign-in FAILED: {name} from {ip}")
            return self.send(401, "Wrong user name or password\n", "text/plain")
        cred = json.loads(self.body())
        client = json.loads(unb64(cred["response"]["clientDataJSON"]))
        name = challenges.pop(client.get("challenge"), "?")
        if name == "?":
            log("rejected: unknown or reused challenge")
            return self.send(400, {"message": "rejected: unknown challenge"})
        if path == "/api/register/finish":
            v = verify_registration_response(credential=cred, expected_challenge=unb64(client["challenge"]),
                                             expected_rp_id=SITE, expected_origin=ORIGIN)
            all_users = users()
            all_users[name]["passkeys"] = [{"credential_id": b64(v.credential_id),
                                            "public_key": b64(v.credential_public_key), "sign_count": v.sign_count}]
            save(all_users)
            log(f"passkey added: {name} (stored: public key only)")
            return self.send(200, {"message": f"Passkey saved for {SITE}"})
        if path == "/api/login/finish":
            all_users = users()
            owner = next((n for n, u in all_users.items() for p in u.get("passkeys", [])
                          if p["credential_id"] == cred["id"]), None)
            if not owner:
                log("rejected: unknown passkey")
                return self.send(400, {"message": "rejected: unknown passkey"})
            pk = next(p for p in all_users[owner]["passkeys"] if p["credential_id"] == cred["id"])
            try:
                v = verify_authentication_response(
                    credential=cred, expected_challenge=unb64(client["challenge"]), expected_rp_id=SITE,
                    expected_origin=ORIGIN, credential_public_key=unb64(pk["public_key"]),
                    credential_current_sign_count=pk["sign_count"])
            except Exception as e:                              # wrong origin, wrong site, bad signature...
                log(f"rejected: {e}")
                return self.send(400, {"message": f"rejected: {e}"})
            pk["sign_count"] = v.new_sign_count
            save(all_users)
            log(f"passkey sign-in OK: {owner} (origin {client['origin']}, challenge matched, signature valid)")
            return self.send(200, {"message": f"Welcome back, {owner}"})
        self.send(404, {"message": "not found"})


if __name__ == "__main__":
    if SITE == "shop.test" and not os.path.exists(DATA):       # Ana's account from before passkeys: a password
        salt = os.urandom(16)
        save({"ana": {"id": b64(os.urandom(16)), "salt": b64(salt), "pw": pw_hash(os.environ["ANA_PW"], salt)}})
    srv = ThreadingHTTPServer(("0.0.0.0", 443), Handler)
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain("/srv/tls/site.crt", "/srv/tls/site.key")
    srv.socket = ctx.wrap_socket(srv.socket, server_side=True)
    log(f"{SITE} listening on https://{SITE}")
    srv.serve_forever()
