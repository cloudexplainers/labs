"""The scale house's weighbridge PC: the last weights it read (port 80)."""
from http.server import BaseHTTPRequestHandler, HTTPServer


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = b"Last weight: car 4417, 61.2 tonnes\n"
        self.send_response(200)
        self.end_headers()
        self.wfile.write(body)


HTTPServer(("0.0.0.0", 80), Handler).serve_forever()
