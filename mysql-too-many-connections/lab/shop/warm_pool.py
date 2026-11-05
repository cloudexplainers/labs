"""One copy of the shop starting up: it opens its whole pool at once and keeps it ready."""
import sys
import time
from sqlalchemy import create_engine, text
from db import URL

size = int(sys.argv[1])
pool = create_engine(URL, pool_size=size, max_overflow=0)
held = []
try:
    for _ in range(size):
        held.append(pool.connect())
    print(f"pool ready: {size} connections")
except Exception as e:
    print(f"opened {len(held)} of {size}, then: {e.orig.args}")
for c in held:
    c.close()                      # back into the pool: still connected, idle
sys.stdout.flush()
try:
    time.sleep(10**6)
except KeyboardInterrupt:
    print("stopped")
