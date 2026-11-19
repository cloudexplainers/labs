# The online menu of a small taco truck, Ana's Tacos.
import signal
import socket
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

VERSION = "1.1"
TACOS = ["Carnitas", "Al pastor", "Black bean", "Fish"]


class Menu(BaseHTTPRequestHandler):
    def do_GET(self):
        lines = [f"Ana's Tacos, menu {VERSION}"] + [f"{i}. {t}" for i, t in enumerate(TACOS, 1)]
        body = "\n".join(lines) + f"\nserved by {socket.gethostname()}\n"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(body.encode())


signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))
print(f"menu {VERSION} listening on port 8080", flush=True)
HTTPServer(("", 8080), Menu).serve_forever()
