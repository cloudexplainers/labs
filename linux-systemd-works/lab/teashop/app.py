"""Ana's tea shop: a tiny web page on port 8080, plus a helper that refreshes the stock list."""
import subprocess

from http.server import BaseHTTPRequestHandler, HTTPServer

helper = subprocess.Popen(["python3", "refresher.py"])


class Shop(BaseHTTPRequestHandler):
    def do_GET(self):
        body = b"Ana's Tea Shop: 12 teas in stock\n"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


print("Tea shop open on port 8080", flush=True)
HTTPServer(("", 8080), Shop).serve_forever()
