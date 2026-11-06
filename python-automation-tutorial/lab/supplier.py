"""Highland Leaf Co., Ana's (made-up) tea supplier, for P092. Runs off-screen on 127.0.0.1:8000 inside the lab.

  GET  /api/stock          JSON stock list; needs the header X-API-Key: demo-key-123, else 401
  GET  /portal             the wholesale portal's sign-in page (no API: a person, or a browser script, signs in)
  POST /portal/login       username ana + password leaf-and-kettle sets a session cookie
  GET  /portal/deliveries  Ana's open deliveries (a table), and a link to download the price list
  GET  /portal/prices.csv  the price list, as a download
Standard library only. Both secrets are made up for the lab.
"""
import json
import secrets
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs

API_KEY, USER, PASSWORD = "demo-key-123", "ana", "leaf-and-kettle"
SESSIONS: set[str] = set()
STOCK = [{"tea": "Earl Grey", "kg": 42}, {"tea": "Sencha", "kg": 8}, {"tea": "Darjeeling", "kg": 15},
         {"tea": "Rooibos", "kg": 60}, {"tea": "Jasmine Pearls", "kg": 3}, {"tea": "Masala Chai", "kg": 27}]
DELIVERIES = [("HL-1071", "Earl Grey, 5 kg", "Shipped", "Nov 9"),
              ("HL-1072", "Jasmine Pearls, 1 kg", "Packing", "Nov 12")]
PRICES = "tea,price_per_kg\nEarl Grey,28.00\nSencha,39.00\nDarjeeling,52.00\nRooibos,22.00\n" \
         "Jasmine Pearls,61.50\nMasala Chai,26.50\n"
STYLE = "<style>body{font:18px sans-serif;margin:40px}td,th{padding:6px 14px;border-bottom:1px solid #ccc}</style>"


def page(body: str) -> bytes:
    return f"<!doctype html><title>Highland Leaf portal</title>{STYLE}<h1>Highland Leaf Co.</h1>{body}".encode()


SIGN_IN = ('<form method="post" action="/portal/login"><p><label>Username <input name="username"></label></p>'
           '<p><label>Password <input name="password" type="password"></label></p>'
           '<p><button>Sign in</button></p></form>')


class Handler(BaseHTTPRequestHandler):
    def send(self, code: int, body: bytes, ctype="text/html", headers=()):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        for k, v in headers:
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def signed_in(self) -> bool:
        cookie = self.headers.get("Cookie", "")
        return any(c.strip().removeprefix("session=") in SESSIONS for c in cookie.split(";") if "session=" in c)

    def do_GET(self):
        if self.path == "/api/stock":
            if self.headers.get("X-API-Key") != API_KEY:
                return self.send(401, b'{"error": "missing or wrong API key"}', "application/json")
            return self.send(200, json.dumps(STOCK).encode(), "application/json")
        if self.path == "/portal":
            return self.send(200, page("<h2>Sign in</h2>" + SIGN_IN))
        if self.path == "/portal/deliveries":
            if not self.signed_in():
                return self.send(303, b"", headers=[("Location", "/portal")])
            rows = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a, b, c, d in DELIVERIES)
            return self.send(200, page("<h2>Your deliveries</h2><table><tr><th>Order</th><th>Items</th>"
                                       f"<th>Status</th><th>Arrives</th></tr>{rows}</table>"
                                       '<p><a href="/portal/prices.csv">Download price list</a></p>'))
        if self.path == "/portal/prices.csv":
            if not self.signed_in():
                return self.send(303, b"", headers=[("Location", "/portal")])
            return self.send(200, PRICES.encode(), "text/csv",
                             [("Content-Disposition", 'attachment; filename="highland-prices.csv"')])
        self.send(404, page("<p>Not found</p>"))

    def do_POST(self):
        if self.path != "/portal/login":
            return self.send(404, page("<p>Not found</p>"))
        form = parse_qs(self.rfile.read(int(self.headers.get("Content-Length", 0))).decode())
        if form.get("username") == [USER] and form.get("password") == [PASSWORD]:
            sid = secrets.token_hex(8)
            SESSIONS.add(sid)
            return self.send(303, b"", headers=[("Location", "/portal/deliveries"),
                                                ("Set-Cookie", f"session={sid}; Path=/; HttpOnly")])
        self.send(200, page('<p class="error">Wrong username or password</p>' + SIGN_IN))

    def log_message(self, *a):
        pass


ThreadingHTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
