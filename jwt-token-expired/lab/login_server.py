#!/usr/bin/env python3
"""The shop's login server (lab only). POST /login gives an access token (a JWT, 5 minutes) and a refresh token
(a random string the server remembers, 7 days). POST /refresh trades a refresh token for a new access token.
Tokens are signed with HS256 and a secret shared with the shop API (/srv/secret)."""
import json
import os
import secrets
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import jwt

SECRET = open("/srv/secret").read().strip()
ACCESS_SECONDS = int(os.environ.get("ACCESS_SECONDS", "300"))
REFRESH_SECONDS = 7 * 24 * 3600
USERS = {"ana": "kettle-2026"}
refresh_tokens = {}   # refresh token -> (user, expiry): stored, so the server can revoke one


def access_token(user: str) -> str:
    now = int(time.time())
    return jwt.encode({"sub": user, "iat": now, "exp": now + ACCESS_SECONDS}, SECRET, algorithm="HS256")


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    server_version = "login"
    sys_version = ""

    def reply(self, code: int, body: dict):
        data = (json.dumps(body) + "\n").encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
        if self.path == "/login":
            user = body.get("user")
            if USERS.get(user) != body.get("password"):
                return self.reply(401, {"error": "invalid_credentials"})
            rt = secrets.token_urlsafe(24)
            refresh_tokens[rt] = (user, time.time() + REFRESH_SECONDS)
            return self.reply(200, {"access_token": access_token(user), "expires_in": ACCESS_SECONDS,
                                    "refresh_token": rt})
        if self.path == "/refresh":
            user, until = refresh_tokens.get(body.get("refresh_token"), (None, 0))
            if not user or time.time() > until:
                return self.reply(401, {"error": "invalid_grant", "message": "log in again"})
            return self.reply(200, {"access_token": access_token(user), "expires_in": ACCESS_SECONDS})
        self.reply(404, {"error": "not_found"})

    def do_GET(self):
        self.reply(404, {"error": "not_found"})

    def log_message(self, fmt, *args):
        pass


ThreadingHTTPServer(("0.0.0.0", 80), Handler).serve_forever()
