#!/usr/bin/env python3
"""Ana's tea shop app for P064 (runs as user "shop" under systemd, on 127.0.0.1:8080).

POST /order with tea=<name>: saves a session file (one per visitor), appends the order to orders.txt and writes a
line to its request log. Like most servers it opens its log once at start and keeps it open, which is what makes a
deleted log keep its space. Any failure to save is answered with the real error text.
"""
import datetime
import os
import secrets
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

DATA = "/var/lib/shop"
LOG = open("/var/log/shop/access.log", "a", buffering=1)


class Shop(BaseHTTPRequestHandler):
    def do_POST(self):
        body = self.rfile.read(int(self.headers.get("Content-Length") or 0)).decode()
        tea = parse_qs(body).get("tea", ["?"])[0]
        try:
            with open(f"{DATA}/sessions/sess_{secrets.token_hex(8)}", "w") as f:
                f.write(f"cart={tea}\n")
            with open(f"{DATA}/orders.txt", "a") as f:
                f.write(f"{datetime.datetime.now():%Y-%m-%d %H:%M} {tea}\n")
            code, reply = 200, f"order saved: {tea}\n"
        except OSError as e:
            code, reply = 500, f"could not save the order: {e.strerror}\n"
            print(f"order failed: {e}", flush=True)
        try:
            stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%d/%b/%Y:%H:%M:%S +0000")
            LOG.write(f'{self.client_address[0]} - - [{stamp}] "POST /order HTTP/1.1" {code} tea={tea}\n')
        except OSError:
            pass
        self.send_response(code)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(reply.encode())

    def log_message(self, *a):
        pass


HTTPServer(("127.0.0.1", 8080), Shop).serve_forever()
