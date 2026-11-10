"""Shared by the lab's three small services: a log file, saved files, a plain HTML page and HTTPS serving."""
import json
import os
import ssl
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ISSUER = "https://id.maple.test/realms/maple"
OIDC = ISSUER + "/protocol/openid-connect"
CA = "/etc/ssl/certs/ca-certificates.crt"
DATA = "/srv/data"
CALENDAR = "https://calendar.maple.test"

PAGE = """<!doctype html><html><head><meta charset="utf-8"><title>{title}</title>
<style>body{{font:34px/1.45 system-ui,sans-serif;margin:0;background:#f6f7f9;color:#1b2430}}
header{{background:{color};color:#fff;padding:26px 64px;font-size:40px;font-weight:700}}
main{{max-width:1180px;margin:70px auto;background:#fff;border-radius:18px;padding:56px 64px;box-shadow:0 2px 14px #0002}}
h1{{margin:0 0 18px;font-size:76px;line-height:1.1}} p{{margin:14px 0;font-size:40px}}
a.btn{{display:inline-block;margin:22px 18px 0 0;padding:18px 32px;border-radius:12px;background:{color};color:#fff;
text-decoration:none;font-weight:600;font-size:34px}}</style></head>
<body><header>{title}</header><main><h1><span id="h">{h1}</span></h1>{body}</main></body></html>"""


def logger(name):
    def log(msg):
        with open(f"/srv/log/{name}.log", "a") as f:
            f.write(f"{time.strftime('%H:%M:%S')} {msg}\n")
    return log


def save(name, obj, mode=0o644):
    path = os.path.join(DATA, name)
    with open(path, "w") as f:
        f.write(obj if isinstance(obj, str) else json.dumps(obj, indent=1))
    os.chmod(path, mode)
    os.chown(path, 1000, 1000)


class Handler(BaseHTTPRequestHandler):
    title, color = "App", "#345"

    def page(self, code, h1, body="", headers=()):
        raw = PAGE.format(title=self.title, color=self.color, h1=h1, body=body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        for k, v in headers:
            self.send_header(k, v)
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def json(self, code, obj, headers=()):
        raw = (json.dumps(obj, indent=1) + "\n").encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        for k, v in headers:
            self.send_header(k, v)
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def redirect(self, to, headers=()):
        self.send_response(302)
        self.send_header("Location", to)
        for k, v in headers:
            self.send_header(k, v)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def log_message(self, *a):
        pass

    def sid(self):
        for part in self.headers.get("Cookie", "").split(";"):
            k, _, v = part.strip().partition("=")
            if k == "sid":
                return v
        return None


def serve(handler, name):
    httpd = ThreadingHTTPServer(("0.0.0.0", 443), handler)
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain("/srv/tls/site.crt", "/srv/tls/site.key")
    httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)
    print(f"listening on https://{name}", flush=True)
    httpd.serve_forever()
