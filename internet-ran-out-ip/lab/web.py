#!/usr/bin/env python3
"""A tiny web server that answers over IPv4 and IPv6 and prints who visited.  Usage: python3 web.py PORT TEXT"""
import socket
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT, TEXT = int(sys.argv[1]), " ".join(sys.argv[2:])


class Server(ThreadingHTTPServer):
    address_family = socket.AF_INET6

    def server_bind(self):
        self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)   # IPv4 visitors too
        super().server_bind()


class Page(BaseHTTPRequestHandler):
    def do_GET(self):
        who = self.client_address[0].removeprefix("::ffff:")   # an IPv4 visitor, as plain IPv4
        print(f"visit from {who}", flush=True)
        body = (TEXT + "\n").encode()
        self.send_response(200)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


if not socket.has_ipv6 or not __import__("os").path.exists("/proc/sys/net/ipv6"):
    Server.address_family = socket.AF_INET                            # a machine with no IPv6 at all
    Server.server_bind = ThreadingHTTPServer.server_bind
print(f"listening on port {PORT}", flush=True)
try:
    Server(("::" if Server.address_family == socket.AF_INET6 else "0.0.0.0", PORT), Page).serve_forever()
except KeyboardInterrupt:
    pass
