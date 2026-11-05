#!/usr/bin/env python3
"""Count IANA's 256 IPv4 blocks by status.  Usage: python3 blocks.py ipv4-address-space.csv"""
import csv
import sys
from collections import defaultdict

WHAT = {"ALLOCATED": "to the 5 regional registries", "LEGACY": "given out directly, early on",
        "RESERVED": "never for public use"}
rows = list(csv.reader(open(sys.argv[1], newline="")))[1:]
by = defaultdict(list)
for prefix, name, date, *rest in rows:
    status = next(c for c in rest if c in WHAT)
    by[status].append(date)
print(f"{len(rows)} blocks of {2 ** 24:,} addresses")
for status in WHAT:
    print(f"{status:<10} {len(by[status]):>3}  {WHAT[status]}")
print(f"last block given out: {max(by['ALLOCATED'])}")
