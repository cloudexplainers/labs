# The song request board of a small community radio station, Radio Maple FM. Version 2.0: shows the show on air now, from ON_AIR.
import os
import signal
import socket
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

VERSION = "2.0"
ON_AIR = os.environ["ON_AIR"]   # set by the station's ConfigMap
POD = socket.gethostname()
SONGS = ["Blue Monday", "Harvest Moon", "Dancing Queen"]


class Board(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/whoami":
            body = f"{POD} v{VERSION}\n"
            kind = "text/plain"
        else:
            items = "".join(f"<li>{s}</li>" for s in SONGS)
            body = (f"<!doctype html><title>Radio Maple FM</title><h1>Radio Maple FM: song requests</h1>"
                    f"<p>On air now: {ON_AIR}</p><ol>{items}</ol><p>version {VERSION}, served by {POD}</p>")
            kind = "text/html"
        self.send_response(200)
        self.send_header("Content-Type", kind)
        self.end_headers()
        self.wfile.write(body.encode())

    def log_message(self, fmt, *args):
        print(f"{self.address_string()} {fmt % args}", flush=True)


signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))   # stop at once when Kubernetes asks
print(f"request board {VERSION} listening on port 8080", flush=True)
HTTPServer(("", 8080), Board).serve_forever()
