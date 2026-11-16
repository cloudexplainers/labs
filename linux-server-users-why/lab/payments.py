"""A stand-in card payment service: every charge takes about 200 ms, like a real card processor's answer."""
import json
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class Pay(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def do_POST(self):
        self.rfile.read(int(self.headers.get("Content-Length", 0)))
        time.sleep(0.2)
        body = json.dumps({"paid": True}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *a):
        pass


ThreadingHTTPServer.daemon_threads = True
ThreadingHTTPServer.request_queue_size = 1024
ThreadingHTTPServer(("0.0.0.0", 9000), Pay).serve_forever()
