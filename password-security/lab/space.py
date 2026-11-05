#!/usr/bin/env python3
"""How long it takes to try every possible password, at the speed this computer guesses.

Measures guesses a second on one CPU core for a fast hash (SHA-256) and a slow one (Argon2id,
argon2-cffi defaults), then divides the number of possible passwords of each kind by that speed.
"""
import hashlib
import time

from argon2 import PasswordHasher


def per_second(fn, seconds=3.0):
    n, end = 0, time.perf_counter() + seconds
    while time.perf_counter() < end:
        fn(b"sunshine1")
        n += 1
    return n / seconds


def big(n):
    for size, name in ((1e18, "quintillion"), (1e15, "quadrillion"), (1e12, "trillion"), (1e9, "billion"),
                       (1e6, "million"), (1e3, "thousand")):
        if n >= size:
            v = n / size
            return f"{v:.1f} {name}" if v < 10 else f"{v:,.0f} {name}"
    return f"{n:,.0f}"


def span(seconds):
    if seconds < 1:
        return "under 1 second"
    for size, name in ((31_557_600, "years"), (86_400, "days"), (3600, "hours"), (60, "minutes")):
        if seconds >= size:
            v = seconds / size
            return f"{big(v)} {name}" if v >= 1e6 else f"{v:.1f} {name}" if v < 10 else f"{v:,.0f} {name}"
    return f"{seconds:.0f} seconds"


ph = PasswordHasher()
fast = per_second(lambda p: hashlib.sha256(p).digest())
slow = per_second(lambda p: ph.hash(p))
print("Guesses a second, one CPU core:")
print(f"  SHA-256 (fast):  {fast:>11,.0f}")
print(f"  Argon2id (slow): {slow:>11,.0f}")
print()
rows = [("10,000 common ones", 10_000), ("8 lowercase", 26 ** 8), ("8 of any 95 keys", 95 ** 8),
        ("12 lowercase", 26 ** 12), ("5 random words", 7776 ** 5)]
print(f"{'Password':<20}{'Possible':<17}{'SHA-256':<16}Argon2id")
for name, n in rows:
    print(f"{name:<20}{big(n):<17}{span(n / fast):<16}{span(n / slow)}")
