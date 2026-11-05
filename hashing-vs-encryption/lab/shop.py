#!/usr/bin/env python3
"""Ana's shop accounts: passwords are stored only as Argon2id hashes (argon2-cffi 21.1 defaults on Ubuntu 24.04: 100 MiB, 2 passes, 8 lanes; above OWASP's minimum).
Usage: python3 shop.py signup NAME PASSWORD | python3 shop.py login NAME PASSWORD"""
import sys
from pathlib import Path

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

DB = Path("accounts.txt")
ph = PasswordHasher()
action, name, password = sys.argv[1:4]
accounts = dict(l.split(" ", 1) for l in DB.read_text().splitlines()) if DB.exists() else {}

if action == "signup":
    accounts[name] = ph.hash(password)
    DB.write_text("".join(f"{n} {h}\n" for n, h in accounts.items()))
    print(f"saved {name}: password stored as a hash")
elif action == "login":
    try:
        ph.verify(accounts[name], password)
        print(f"welcome back, {name}")
    except VerifyMismatchError:
        print("wrong password")
