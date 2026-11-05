#!/usr/bin/env python3
"""Show an IP address the way the network stores it: as bits.  Usage: python3 bits.py ADDRESS"""
import ipaddress
import sys

addr = ipaddress.ip_address(sys.argv[1])
bits = f"{int(addr):0{addr.max_prefixlen}b}"
if addr.version == 4:
    print(".".join(bits[i:i + 8] for i in range(0, 32, 8)))
else:
    print(addr.exploded)
print(f"{addr.max_prefixlen} bits")
