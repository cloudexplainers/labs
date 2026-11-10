"""Check a SAML 2.0 response the way a service provider must: signature first, then what the signed part says."""
import datetime
import functools

import requests
from lxml import etree
from signxml import XMLVerifier

NS = {"samlp": "urn:oasis:names:tc:SAML:2.0:protocol", "saml": "urn:oasis:names:tc:SAML:2.0:assertion",
      "ds": "http://www.w3.org/2000/09/xmldsig#", "md": "urn:oasis:names:tc:SAML:2.0:metadata"}
ISSUER = "https://id.maple.test/realms/maple"
CA = "/etc/ssl/certs/ca-certificates.crt"


class Refused(Exception):
    pass


@functools.cache
def idp_cert() -> str:
    """Maple ID's signing certificate, from its published SAML metadata (fetched over HTTPS once)."""
    r = requests.get(ISSUER + "/protocol/saml/descriptor", verify=CA)
    r.raise_for_status()
    cert = etree.fromstring(r.content).find(".//ds:X509Certificate", NS).text.strip()
    return "-----BEGIN CERTIFICATE-----\n" + cert + "\n-----END CERTIFICATE-----\n"


def verified_assertion(xml: bytes):
    """The assertion element exactly as the signature covers it, or Refused."""
    root = etree.fromstring(xml)
    status = root.find("samlp:Status/samlp:StatusCode", NS)
    if status is None or not status.get("Value", "").endswith(":Success"):
        raise Refused("the response's status is not Success")
    assertion = root.find("saml:Assertion", NS)
    if assertion is None or assertion.find("ds:Signature", NS) is None:
        raise Refused("no signed assertion in the response")
    try:
        signed = XMLVerifier().verify(etree.tostring(assertion), x509_cert=idp_cert()).signed_xml
    except Exception as e:
        raise Refused(f"signature check failed ({type(e).__name__})") from None
    method = assertion.find("ds:Signature/ds:SignedInfo/ds:SignatureMethod", NS).get("Algorithm").split("#")[-1]
    signed.set("{lab}signature-method", method)       # remembered for saml-show; not part of the signed data
    return signed


def facts(a) -> dict:
    cond = a.find("saml:Conditions", NS)
    conf = a.find("saml:Subject/saml:SubjectConfirmation/saml:SubjectConfirmationData", NS)
    return {
        "issuer": a.findtext("saml:Issuer", namespaces=NS),
        "name_id": a.findtext("saml:Subject/saml:NameID", namespaces=NS),
        "audience": a.findtext("saml:Conditions/saml:AudienceRestriction/saml:Audience", namespaces=NS),
        "not_before": cond.get("NotBefore"), "not_on_or_after": cond.get("NotOnOrAfter"),
        "recipient": conf.get("Recipient"), "in_response_to": conf.get("InResponseTo"),
        "attributes": {at.get("Name"): at.findtext("saml:AttributeValue", namespaces=NS)
                       for at in a.findall("saml:AttributeStatement/saml:Attribute", NS)},
        "signature_method": a.get("{lab}signature-method"),
    }


def when(s: str) -> datetime.datetime:
    return datetime.datetime.fromisoformat(s.replace("Z", "+00:00"))


def check(xml: bytes, audience: str, destination: str, in_response_to):
    a = facts(verified_assertion(xml))
    now = datetime.datetime.now(datetime.timezone.utc)
    if a["issuer"] != ISSUER:
        raise Refused(f"issuer is {a['issuer']}, not Maple ID")
    if a["audience"] != audience:
        raise Refused(f"audience is {a['audience']}: this assertion was written for another site")
    if a["recipient"] != destination:
        raise Refused("recipient is another address")
    if not (when(a["not_before"]) - datetime.timedelta(seconds=5) <= now < when(a["not_on_or_after"])):
        raise Refused("outside the assertion's time window")
    if not in_response_to or a["in_response_to"] != in_response_to:
        raise Refused("this response doesn't answer a request this browser started")
    return a
