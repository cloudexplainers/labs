"""The building's laundry booking page (port 8080): who has which machine when. Made-up tenants."""
from http.server import BaseHTTPRequestHandler, HTTPServer

PAGE = """<!doctype html><title>Laundry room bookings</title>
<h1>Maple Court laundry room</h1>
<p>Saturday bookings</p>
<ul><li>Washer 1, 9:00 - Apartment 2B</li><li>Washer 2, 10:00 - Apartment 4A</li><li>Dryer 1, 11:00 - Apartment 3C</li></ul>
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


HTTPServer(("0.0.0.0", 8080), H).serve_forever()
