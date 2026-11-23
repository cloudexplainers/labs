"""Certificates for P131's lab, made at image build time with the cryptography package.

coop-root-ca.crt   "Valley Dairy Co-op Root CA": the co-op's own certificate authority (private, in no trust store)
portal.crt/.key    portal.coop.lan, signed by the co-op CA, valid for a year from the build
tank.crt/.key      tank.coop.lan, signed by the co-op CA, expired: valid 2025-10-01 to 2026-10-01
office-proxy.pem   "Valley Dairy Co-op Office Inspection CA": key + certificate for the office network's TLS inspection
                   proxy (mitmproxy reads it as mitmproxy-ca.pem); office-proxy-ca.crt is its public part
"""
import datetime as dt
import sys
from pathlib import Path

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.x509.oid import ExtendedKeyUsageOID, NameOID

out = Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)
now = dt.datetime.now(dt.timezone.utc)


def name(cn):
    return x509.Name([x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Valley Dairy Co-op"),
                      x509.NameAttribute(NameOID.COMMON_NAME, cn)])


def pem_key(k):
    return k.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption())


def ca(cn):
    key = ec.generate_private_key(ec.SECP256R1())
    cert = (x509.CertificateBuilder().subject_name(name(cn)).issuer_name(name(cn)).public_key(key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(now - dt.timedelta(days=400)).not_valid_after(now + dt.timedelta(days=3650))
            .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
            .add_extension(x509.KeyUsage(False, False, False, False, False, True, True, False, False), critical=True)
            .add_extension(x509.SubjectKeyIdentifier.from_public_key(key.public_key()), critical=False)
            .sign(key, hashes.SHA256()))
    return key, cert


def leaf(host, ca_key, ca_cert, start, end):
    key = ec.generate_private_key(ec.SECP256R1())
    cert = (x509.CertificateBuilder().subject_name(name(host)).issuer_name(ca_cert.subject)
            .public_key(key.public_key()).serial_number(x509.random_serial_number())
            .not_valid_before(start).not_valid_after(end)
            .add_extension(x509.SubjectAlternativeName([x509.DNSName(host)]), critical=False)
            .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
            .add_extension(x509.ExtendedKeyUsage([ExtendedKeyUsageOID.SERVER_AUTH]), critical=False)
            .add_extension(x509.AuthorityKeyIdentifier.from_issuer_public_key(ca_key.public_key()), critical=False)
            .sign(ca_key, hashes.SHA256()))
    return key, cert


ck, cc = ca("Valley Dairy Co-op Root CA")
(out / "coop-root-ca.crt").write_bytes(cc.public_bytes(serialization.Encoding.PEM))
for host, start, end, stem in [
    ("portal.coop.lan", now - dt.timedelta(days=1), now + dt.timedelta(days=365), "portal"),
    ("tank.coop.lan", dt.datetime(2025, 10, 1, tzinfo=dt.timezone.utc), dt.datetime(2026, 10, 1, tzinfo=dt.timezone.utc), "tank"),
]:
    k, c = leaf(host, ck, cc, start, end)
    (out / f"{stem}.key").write_bytes(pem_key(k))
    (out / f"{stem}.crt").write_bytes(c.public_bytes(serialization.Encoding.PEM))
pk, pc = ca("Valley Dairy Co-op Office Inspection CA")
(out / "office-proxy.pem").write_bytes(pem_key(pk) + pc.public_bytes(serialization.Encoding.PEM))
(out / "office-proxy-ca.crt").write_bytes(pc.public_bytes(serialization.Encoding.PEM))
print("certificates in", out)
