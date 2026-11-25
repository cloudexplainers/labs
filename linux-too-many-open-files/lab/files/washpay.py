"""The laundromat's payment server: each washer and dryer's card reader posts a payment here (port 8000)."""
import logging
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

paid = 0


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        global paid
        machine = self.path.split("/")[-1]   # /pay/washer-07
        log = logging.getLogger(machine)
        path = f"/var/log/washpay/{machine}.log"
        log.addHandler(logging.FileHandler(path))
        log.warning("paid $3.50")
        paid += 1
        self.send_response(200)
        self.end_headers()
        self.wfile.write(f"paid, payment {paid}\n".encode())

    def log_message(self, *args):
        pass


ThreadingHTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
