"""The freight yard's railcar tracker: which cars stand on which track (port 8080, every address)."""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

CARS = {"track 3": 12, "track 5": 8, "track 7": 15}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = json.dumps(CARS).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)


HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
