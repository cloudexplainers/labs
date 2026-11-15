from http.server import BaseHTTPRequestHandler, HTTPServer


class Deploy(BaseHTTPRequestHandler):
    def do_GET(self):
        body = b"staging: deployed\n" if self.path == "/deploy" else b"staging server\n"
        self.send_response(200)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


HTTPServer(("", 8000), Deploy).serve_forever()
