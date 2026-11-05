#!/usr/bin/env python3
"""Off-screen (run as user shop): grow the shop's request log until the disk refuses, the way weeks of busy
traffic with every request logged would, but in seconds. Prints how many bytes it added."""
import datetime
import random

TEAS = ["sencha", "matcha", "earl-grey", "assam", "oolong", "rooibos", "chai", "darjeeling"]
start = datetime.datetime(2026, 10, 1, tzinfo=datetime.timezone.utc)
log = open("/var/log/shop/access.log", "a")
added, t = 0, start
while True:
    lines = []
    for _ in range(8000):
        t += datetime.timedelta(milliseconds=random.randint(5, 400))
        ip = f"198.51.100.{random.randint(2, 254)}"
        page = random.choice(["GET /", "GET /teas", f"GET /teas/{random.choice(TEAS)}",
                              f"POST /order", "GET /cart"])
        code = 200
        lines.append(f'{ip} - - [{t:%d/%b/%Y:%H:%M:%S +0000}] "{page} HTTP/1.1" {code} '
                     f'agent="Mozilla/5.0 (X11; Linux x86_64)" ms={random.randint(3, 90)}\n')
    chunk = "".join(lines)
    try:
        log.write(chunk)
        log.flush()
        added += len(chunk)
    except OSError as e:
        print(f"stopped: {e}; added {added} bytes")
        break
