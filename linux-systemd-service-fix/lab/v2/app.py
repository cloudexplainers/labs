"""Ana's tea shop, version 2: the stock file's path now comes from an environment variable."""
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

# TEA_STOCK is set in Ana's ~/.bashrc
stock_file = os.environ["TEA_STOCK"]
teas = open(stock_file).read().split()


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
