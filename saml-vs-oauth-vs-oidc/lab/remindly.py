#!/usr/bin/env python3
"""Remindly: a small appointment-reminder app (remindly.test). It uses Maple ID two ways:

  /connect-calendar   plain OAuth 2.0 (authorization code + PKCE), scope calendar.read: permission to read the
                      clinic's calendar through Maple's calendar API. No `openid` scope, so no ID token comes back.
  /login              OpenID Connect: the same flow with scope `openid profile email`; an ID token comes back and
                      Remindly checks its signature, issuer, audience and nonce before it trusts the name in it.
  /callback           Maple ID sends the browser back here with a one-time code for either flow.
Remindly never sees Ana's Maple ID password. Every step goes to /srv/log/remindly.log.
"""
import base64
import hashlib
import os
import secrets
import ssl
import urllib.parse

import jwt
import requests

from common import CA, CALENDAR, ISSUER, OIDC, Handler, logger, save, serve

CLIENT_ID = "remindly"
SECRET = os.environ["CLIENT_SECRET"]
REDIRECT = "https://remindly.test/callback"
log = logger("remindly")
sessions = {}
SCOPES = {"connect": "calendar.read", "login": "openid profile email"}


def b64url(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode()


class Remindly(Handler):
    title, color = "Remindly", "#5a4fcf"

    def do_GET(self):
        url = urllib.parse.urlparse(self.path)
        q = dict(urllib.parse.parse_qsl(url.query))
        if url.path == "/":
            return self.page(200, "Appointment reminders, sent for you",
                             '<a class="btn" id="connect" href="/connect-calendar">Connect your Maple calendar</a> '
                             '<a class="btn" id="signin" href="/login">Sign in with Maple ID</a>')
        if url.path in ("/connect-calendar", "/login"):
            flow = "connect" if url.path == "/connect-calendar" else "login"
            sid = secrets.token_urlsafe(16)
            state, nonce, verifier = secrets.token_urlsafe(16), secrets.token_urlsafe(16), secrets.token_urlsafe(48)
            sessions[sid] = {"flow": flow, "state": state, "nonce": nonce, "verifier": verifier}
            params = {"response_type": "code", "client_id": CLIENT_ID, "redirect_uri": REDIRECT,
                      "scope": SCOPES[flow], "state": state,
                      "code_challenge": b64url(hashlib.sha256(verifier.encode()).digest()),
                      "code_challenge_method": "S256"}
            if flow == "login":
                params["nonce"] = nonce
            log(f"{flow}: sent the browser to id.maple.test asking for scope \"{SCOPES[flow]}\"")
            return self.redirect(OIDC + "/auth?" + urllib.parse.urlencode(params),
                                 [("Set-Cookie", f"sid={sid}; Path=/; HttpOnly; Secure; SameSite=Lax")])
        if url.path == "/callback":
            s = sessions.pop(self.sid() or "", None)
            if "error" in q:
                log(f"callback: Maple ID said {q['error']}")
                return self.page(400, "Cancelled", f"<p>{q['error']}</p>")
            if not s or q.get("state") != s["state"]:
                log("callback refused: the state doesn't match a request this browser started")
                return self.page(400, "Refused", "<p>This wasn't started here.</p>")
            r = requests.post(OIDC + "/token", auth=(CLIENT_ID, SECRET), verify=CA, data={
                "grant_type": "authorization_code", "code": q["code"], "redirect_uri": REDIRECT,
                "code_verifier": s["verifier"]})
            if r.status_code != 200:
                log(f"token: Maple ID answered {r.status_code}: {r.text}")
                return self.page(400, "Failed", f"<p>{r.text}</p>")
            tok = r.json()
            got = [k for k in ("access_token", "id_token") if k in tok]
            log(f"token: swapped the one-time code; got {' and '.join(got).replace('_', ' ')} (scope \"{tok.get('scope')}\")")
            if s["flow"] == "connect":
                save("oauth_tokens.json", tok, 0o600)
                save("access_token", tok["access_token"], 0o600)
                ev = requests.get(CALENDAR + "/events", verify=CA,
                                  headers={"Authorization": "Bearer " + tok["access_token"]})
                n = len(ev.json().get("events", [])) if ev.status_code == 200 else 0
                log(f"calendar API: GET /events -> {ev.status_code}, {n} appointments")
                return self.page(200, "Calendar connected",
                                 f'<p><span id="count">{n} appointments today.</span> Reminders go out an hour before each.</p>')
            idt = tok["id_token"]
            jwks = jwt.PyJWKClient(OIDC + "/certs", ssl_context=ssl.create_default_context(cafile=CA))
            claims = jwt.decode(idt, jwks.get_signing_key_from_jwt(idt).key, algorithms=["RS256"],
                                audience=CLIENT_ID, issuer=ISSUER)
            if claims.get("nonce") != s["nonce"]:
                log("id token refused: nonce doesn't match")
                return self.page(400, "Refused", "<p>nonce</p>")
            log("id token: signature valid, issuer Maple ID, audience remindly, nonce matched")
            save("oidc_tokens.json", tok, 0o600)
            save("id_token", idt, 0o600)
            save("id_token.json", claims)
            log(f"signed in: {claims.get('name')} <{claims.get('email')}>")
            return self.page(200, f"Welcome, {claims.get('given_name')}",
                             f'<p><span id="who">Signed in as {claims.get("email")}</span></p>')
        return self.page(404, "Not found")


serve(Remindly, "remindly.test")
