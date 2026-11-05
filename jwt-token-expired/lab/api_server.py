#!/usr/bin/env python3
"""The shop API (lab only). GET /orders needs "Authorization: Bearer <access token>". The token is checked with the
secret shared with the login server: the signature first, then exp against this server's own clock."""
import json
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import jwt

SECRET = open("/srv/secret").read().strip()
ORDERS = [{"id": 1041, "item": "Copper kettle", "total": 89.0},
          {"id": 1042, "item": "Glass kettle", "total": 54.0},
          {"id": 1043, "item": "Travel kettle", "total": 32.5}]


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    server_version = "shop-api"
    sys_version = ""

    def reply(self, code: int, body: dict, error: str = ""):
        data = (json.dumps(body) + "\n").encode()
        self.send_response(code)
        if error:
            self.send_header("WWW-Authenticate", f'Bearer error="invalid_token", error_description="{error}"')
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path != "/orders":
            return self.reply(404, {"error": "not_found"})
        auth = self.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return self.reply(401, {"error": "missing_token"}, "No access token")
        try:
            claims = jwt.decode(auth[7:], SECRET, algorithms=["HS256"], leeway=30)
        except jwt.ExpiredSignatureError:
            return self.reply(401, {"error": "token_expired", "message": "Signature has expired"},
                              "The access token expired")
        except jwt.InvalidTokenError as e:
            return self.reply(401, {"error": "invalid_token", "message": str(e)}, "The access token is invalid")
        self.reply(200, {"user": claims["sub"], "orders": ORDERS})

    def log_message(self, fmt, *args):
        pass


ThreadingHTTPServer(("0.0.0.0", 80), Handler).serve_forever()
