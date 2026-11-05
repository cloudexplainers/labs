"""Ana's tea shop website: one page that says which version answered, and which pod served it."""
import os
import signal
import socket
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

VERSION = os.environ.get("VERSION", "1.0")


class Page(BaseHTTPRequestHandler):
    def do_GET(self):
        body = f"Kettle & Bean {VERSION}, served by {socket.gethostname()}\n".encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


# As PID 1 in its container, Python ignores SIGTERM unless it handles it: stop at once when Kubernetes asks.
signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))
HTTPServer(("", 8080), Page).serve_forever()
