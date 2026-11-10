#!/usr/bin/env python3
"""Maple's calendar API (calendar.maple.test): a resource server, in OAuth's words.

It accepts an access token in the Authorization header and checks, per RFC 6750 and RFC 9068: the signature (Maple
ID's published keys), the issuer, that the token was written for this API (audience) and hasn't expired, and that
its scope allows the request: calendar.read to list, calendar.write to add. It never asks who the user is.
"""
import ssl

import jwt

from common import CA, CALENDAR, ISSUER, OIDC, Handler, logger, serve

log = logger("calendar")
EVENTS = [{"time": "09:00", "what": "Check-up, room 1"}, {"time": "10:30", "what": "Filling, room 2"},
          {"time": "14:00", "what": "Cleaning, room 1"}]
jwks = None


def bearer(handler, need):
    global jwks
    auth = handler.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return None, (401, {"error": "no token"}, 'Bearer realm="calendar"')
    tok = auth[7:]
    try:
        jwks = jwks or jwt.PyJWKClient(OIDC + "/certs", ssl_context=ssl.create_default_context(cafile=CA))
        key = jwks.get_signing_key_from_jwt(tok)
        claims = jwt.decode(tok, key.key, algorithms=["RS256"], audience=CALENDAR, issuer=ISSUER)
    except jwt.InvalidAudienceError:
        try:
            aud = jwt.decode(tok, options={"verify_signature": False}).get("aud")
        except Exception:
            aud = None
        d = f"this token was written for {aud}, not for {CALENDAR}"
        return None, (401, {"error": "invalid_token", "error_description": d},
                      f'Bearer error="invalid_token", error_description="{d}"')
    except Exception as e:
        d = f"{type(e).__name__}"
        return None, (401, {"error": "invalid_token", "error_description": d}, 'Bearer error="invalid_token"')
    if need not in claims.get("scope", "").split():
        return None, (403, {"error": "insufficient_scope", "error_description": f"this request needs the scope {need}"},
                      f'Bearer error="insufficient_scope", scope="{need}"')
    return claims, None


class Calendar(Handler):
    def answer(self, need, ok):
        claims, refused = bearer(self, need)
        if refused:
            code, body, www = refused
            log(f"{self.command} {self.path} -> {code} {body['error']}")
            return self.json(code, body, [("WWW-Authenticate", www)])
        log(f"{self.command} {self.path} -> {ok[0]} (scope {claims['scope']})")
        return self.json(*ok)

    def do_GET(self):
        if self.path != "/events":
            return self.json(404, {"error": "not found"})
        return self.answer("calendar.read", (200, {"events": EVENTS}))

    def do_POST(self):
        if self.path != "/events":
            return self.json(404, {"error": "not found"})
        self.rfile.read(int(self.headers.get("Content-Length", 0)))
        return self.answer("calendar.write", (201, {"added": True}))


serve(Calendar, "calendar.maple.test")
