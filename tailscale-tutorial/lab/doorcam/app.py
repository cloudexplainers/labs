"""The front-door camera's recorder (port 80): a status page. It runs no Tailscale."""
from http.server import BaseHTTPRequestHandler, HTTPServer

PAGE = """<!doctype html><title>Door camera</title>
<h1>Front door camera</h1>
<p>Recording: yes. Last motion: 08:42.</p>
"""


class H(BaseHTTPRequestHandler):
    def do_GET(self):
        body = PAGE.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *a):
        pass


HTTPServer(("0.0.0.0", 80), H).serve_forever()
