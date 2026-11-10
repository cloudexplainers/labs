#!/usr/bin/env python3
"""Payroll: the clinic's payroll site. Staff sign in with their Maple ID account through SAML 2.0.

  /           no session: sends the browser to Maple ID with a SAML request (HTTP-Redirect binding)
  /saml/acs   Maple ID has the browser post a SAML response here (HTTP-POST binding): Payroll checks the
              signature with Maple ID's certificate, then the issuer, the audience, the time window and that the
              response answers a request this browser started. Only then is there a session.
Payroll never sees Ana's Maple ID password. Every step goes to /srv/log/payroll.log.
"""
import base64
import datetime
import secrets
import urllib.parse
import zlib

from common import Handler, logger, save, serve
import samlcheck

ENTITY = "https://payroll.test/saml"
ACS = "https://payroll.test/saml/acs"
IDP_SSO = "https://id.maple.test/realms/maple/protocol/saml"
log = logger("payroll")
sessions, pending = {}, {}


class Payroll(Handler):
    title, color = "Payroll", "#2f6f4f"

    def do_GET(self):
        url = urllib.parse.urlparse(self.path)
        if url.path != "/":
            return self.page(404, "Not found")
        who = sessions.get(self.sid() or "")
        if who:
            return self.page(200, f"Welcome, {who['name']}",
                             f"<p><span id=\"who\">Signed in as {who['email']}</span></p><p>Next payday: Friday</p>")
        rid = "_" + secrets.token_hex(16)
        sid = secrets.token_urlsafe(16)
        pending[sid] = rid
        now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        req = (f'<samlp:AuthnRequest xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol" '
               f'xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion" ID="{rid}" Version="2.0" IssueInstant="{now}" '
               f'Destination="{IDP_SSO}" AssertionConsumerServiceURL="{ACS}" '
               f'ProtocolBinding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST">'
               f'<saml:Issuer>{ENTITY}</saml:Issuer></samlp:AuthnRequest>')
        save("saml_request.xml", req)
        deflated = zlib.compress(req.encode())[2:-4]
        to = IDP_SSO + "?" + urllib.parse.urlencode({"SAMLRequest": base64.b64encode(deflated).decode()})
        log(f"no session: sent the browser to id.maple.test with a SAML request ({rid[:7]}...)")
        return self.redirect(to, [("Set-Cookie", f"sid={sid}; Path=/; HttpOnly; Secure; SameSite=None")])

    def do_POST(self):
        if self.path != "/saml/acs":
            return self.page(404, "Not found")
        form = dict(urllib.parse.parse_qsl(self.rfile.read(int(self.headers.get("Content-Length", 0))).decode()))
        xml = base64.b64decode(form.get("SAMLResponse", ""))
        log(f"/saml/acs: the browser posted a SAML response ({len(xml):,} characters of XML)")
        sid = self.sid() or ""
        try:
            a = samlcheck.check(xml, audience=ENTITY, destination=ACS, in_response_to=pending.pop(sid, None))
        except samlcheck.Refused as e:
            log(f"refused: {e}")
            return self.page(403, "Sign-in refused", f"<p>{e}</p>")
        log("signature valid (Maple ID's certificate); issuer, audience and time window checked")
        save("saml_response.xml", xml.decode())
        sessions[sid] = {"email": a["name_id"], "name": f"{a['attributes'].get('firstName', '')} "
                                                         f"{a['attributes'].get('lastName', '')}".strip()}
        log(f"session started for {a['name_id']}")
        return self.redirect("/")


serve(Payroll, "payroll.test")
