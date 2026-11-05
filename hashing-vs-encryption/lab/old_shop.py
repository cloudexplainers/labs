#!/usr/bin/env python3
"""How many sites used to store passwords: one fast SHA-256 hash, no salt. Don't do this.
Usage: python3 old_shop.py signup NAME PASSWORD"""
import hashlib
import sys
from pathlib import Path

DB = Path("old_accounts.txt")
action, name, password = sys.argv[1:4]
assert action == "signup"
with DB.open("a") as f:
    f.write(f"{name} {hashlib.sha256(password.encode()).hexdigest()}\n")
print(f"saved {name}")
