#!/usr/bin/env python3
"""Has this password appeared in a data breach? Uses Have I Been Pwned's Pwned Passwords range API.

The password is hashed here with SHA-1, and only the first 5 of the hash's 40 characters are sent
(k-anonymity): the service answers with every hash it knows that starts with them, and we look for ours.
"""
import hashlib
import sys
import urllib.request

pw = sys.argv[1]
h = hashlib.sha1(pw.encode()).hexdigest().upper()
req = urllib.request.Request(f"https://api.pwnedpasswords.com/range/{h[:5]}",
                             headers={"User-Agent": "cloudexplainers-demo", "Add-Padding": "true"})
body = urllib.request.urlopen(req, timeout=20).read().decode()
count = 0
for line in body.splitlines():
    suffix, n = line.split(":")
    if suffix == h[5:]:
        count = int(n)
print(f"sent only: {h[:5]} (5 of 40 hash characters)")
print(f"seen in breaches: {count:,} times" if count else "seen in breaches: 0 times")
