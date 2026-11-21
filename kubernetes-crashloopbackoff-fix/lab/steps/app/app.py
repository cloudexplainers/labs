# The lane booking board of a small public swimming pool, Riverside Pool.
import os
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer

VERSION = "1.0"
KEY = os.environ["BOOKING_KEY"]          # the key the front desk's till checks
LANES = ["Lane 1: early swim", "Lane 2: lessons", "Lane 3: open"]


class Board(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/healthz":
            body = "ok\n"
        else:
            lines = [f"Riverside Pool lanes {VERSION}"] + LANES
            body = "\n".join(lines) + f"\nserved by {socket.gethostname()}\n"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(body.encode())

    def log_message(self, *args):
        pass


print(f"lane board {VERSION} listening on port 8080", flush=True)
HTTPServer(("", 8080), Board).serve_forever()
