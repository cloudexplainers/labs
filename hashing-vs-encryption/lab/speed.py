#!/usr/bin/env python3
"""How many password hashes this computer makes in a second: fast SHA-256 vs slow Argon2id."""
import hashlib
import time

from argon2 import PasswordHasher


def per_second(fn, seconds=3.0):
    n, end = 0, time.perf_counter() + seconds
    while time.perf_counter() < end:
        fn(b"sunshine1")
        n += 1
    return n / seconds


ph = PasswordHasher()
fast = per_second(lambda p: hashlib.sha256(p).digest())
slow = per_second(lambda p: ph.hash(p))
print(f"SHA-256:  {fast:>12,.0f} hashes a second")
print(f"Argon2id: {slow:>12,.0f} hashes a second")
print(f"Argon2id is {fast / slow:,.0f}x slower")
