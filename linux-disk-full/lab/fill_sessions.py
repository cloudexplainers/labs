#!/usr/bin/env python3
"""Off-screen (run as user shop): one small session file per visitor, never cleaned up, dated over the last
30 days, until the disk has no inodes left. Prints how many files it made."""
import os
import random
import secrets
import time

TEAS = ["sencha", "matcha", "earl-grey", "assam", "oolong", "rooibos", "chai", "darjeeling"]
d = "/var/lib/shop/sessions"
now, made = time.time(), 0
while True:
    p = f"{d}/sess_{secrets.token_hex(8)}"
    try:
        fd = os.open(p, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except OSError as e:
        print(f"stopped: {e}; made {made} files")
        break
    try:
        os.write(fd, f"cart={random.choice(TEAS)}\n".encode())
    except OSError:
        pass
    os.close(fd)
    t = now - random.uniform(0, 30 * 86400)
    os.utime(p, (t, t))
    made += 1
