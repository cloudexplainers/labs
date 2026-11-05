"""A passkey sign-in, checked by a real WebAuthn server library (py_webauthn).

The 'authenticator' here is a small software stand-in for your phone's passkey store. It follows
the WebAuthn rules: a passkey belongs to one site, and the browser writes the page's real address
into the data that gets signed. Test domains only.
   python3 passkey_demo.py register             save a passkey for bank.example
   python3 passkey_demo.py https://PAGE          sign in from that page
   python3 passkey_demo.py https://PAGE --sign-anyway   force a signature (no real browser would)
"""
import base64, hashlib, json, os, sys
from urllib.parse import urlsplit
import cbor2
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from webauthn import verify_authentication_response

STORE = "passkeys.json"
BANK = "bank.example"
b64 = lambda b: base64.urlsafe_b64encode(b).rstrip(b"=").decode()

def register():
    key = ec.generate_private_key(ec.SECP256R1())
    nums = key.public_key().public_numbers()
    cose = cbor2.dumps({1: 2, 3: -7, -1: 1, -2: nums.x.to_bytes(32, "big"), -3: nums.y.to_bytes(32, "big")})
    pem = key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption())
    store = {"site": BANK, "id": b64(os.urandom(16)), "key": pem.decode(), "public": b64(cose)}
    json.dump(store, open(STORE, "w"))
    print(f"passkey saved for: {BANK}")

def sign_in(page, anyway):
    store = json.load(open(STORE))
    page_host = urlsplit(page).hostname
    print(f"browser is on:  {page_host}")
    site = page_host
    if store["site"] != page_host:
        if not anyway:
            print(f"passkeys for {page_host}: none")
            print("nothing to sign, nothing to send")
            return
        site = store["site"]        # pretend the passkey signed for the bank anyway
    challenge = os.urandom(32)      # the bank's one-time challenge
    client = json.dumps({"type": "webauthn.get", "challenge": b64(challenge),
                         "origin": f"https://{page_host}", "crossOrigin": False}).encode()
    auth = hashlib.sha256(site.encode()).digest() + bytes([0x05]) + (1).to_bytes(4, "big")
    key = serialization.load_pem_private_key(store["key"].encode(), None)
    sig = key.sign(auth + hashlib.sha256(client).digest(), ec.ECDSA(hashes.SHA256()))
    print(f"signed address: {json.loads(client)['origin']}")
    cred = {"id": store["id"], "rawId": store["id"], "type": "public-key",
            "response": {"authenticatorData": b64(auth), "clientDataJSON": b64(client), "signature": b64(sig)}}
    try:
        verify_authentication_response(credential=cred, expected_challenge=challenge, expected_rp_id=BANK,
                                       expected_origin=f"https://{BANK}",
                                       credential_public_key=base64.urlsafe_b64decode(store["public"] + "=="),
                                       credential_current_sign_count=0)
        print("bank's server:  ACCEPTED")
    except Exception as e:
        print("bank's server:  REJECTED")
        print(f"reason: {e}")

if sys.argv[1] == "register":
    register()
else:
    sign_in(sys.argv[1], "--sign-anyway" in sys.argv)
