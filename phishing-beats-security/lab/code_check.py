"""What a six-digit code tells the server, and what it doesn't."""
import json
import pyotp

totp = pyotp.TOTP(pyotp.random_base32())   # the secret your phone and the bank share
code = totp.now()                          # what the phone shows right now

sent = {"code": code}                      # everything the login form sends
print(f"phone shows:   {code}")
print(f"form sends:    {json.dumps(sent)}")
print("server check: ", "VALID" if totp.verify(code) else "INVALID")
print("which site was it typed into?", "not in the data" if "site" not in sent else sent["site"])
