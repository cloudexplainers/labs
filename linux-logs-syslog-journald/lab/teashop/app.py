"""Ana's tea shop for P116: a tiny web shop on port 8080 that logs to standard output, like most apps.

Under systemd, everything it prints goes to the journal. A line that starts with <3> is an error and <4> a warning
(systemd reads these syslog level prefixes, SyslogLevelPrefix=yes by default); plain lines are info.
  /            the shop page
  /order?tea=  place an order (Darjeeling is out of stock, so that order fails)
"""
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

STOCK = {"sencha": 40, "assam": 25, "oolong": 12, "darjeeling": 0}
orders = 39


def log(msg, level=""):
    print(f"{level}{msg}", flush=True)


class Shop(BaseHTTPRequestHandler):
    def reply(self, code, text):
        body = (text + "\n").encode()
        self.send_response(code)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        global orders
        url = urlparse(self.path)
        if url.path == "/":
            self.reply(200, f"Ana's Tea Shop: {len(STOCK)} teas")
        elif url.path == "/order":
            tea = parse_qs(url.query).get("tea", [""])[0]
            orders += 1
            if STOCK.get(tea, 0) > 0:
                STOCK[tea] -= 1
                log(f"order {orders} paid: {tea}")
                self.reply(200, f"order {orders}: thank you")
            else:
                log(f"order {orders} failed: {tea} is out of stock", "<3>")
                self.reply(409, f"order {orders}: sorry, {tea} is out of stock")
        else:
            self.reply(404, "not found")

    def log_message(self, *args):        # no access log: the app logs what matters itself
        pass


log("tea shop open on port 8080")
HTTPServer(("127.0.0.1", 8080), Shop).serve_forever()
