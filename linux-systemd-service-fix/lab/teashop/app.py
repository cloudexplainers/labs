"""Ana's tea shop: a tiny web page on port 8080 that lists the teas in stock.txt."""
from http.server import BaseHTTPRequestHandler, HTTPServer

teas = open("stock.txt").read().split()


class Shop(BaseHTTPRequestHandler):
    def do_GET(self):
        body = f"Ana's Tea Shop: {len(teas)} teas in stock\n".encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


print(f"Tea shop open on port 8080 with {len(teas)} teas", flush=True)
HTTPServer(("", 8080), Shop).serve_forever()
