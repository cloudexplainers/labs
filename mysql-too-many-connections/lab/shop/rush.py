"""The ticket sale opens: N customers press Buy at the same moment (one thread each)."""
import sys
import threading
import time
from collections import Counter

n = int(sys.argv[1])
if "--pool" in sys.argv:
    from orders_pool import place_order
else:
    from orders import place_order

results = Counter()
lock = threading.Lock()


def buy(seat):
    try:
        place_order(seat)
        with lock:
            results["placed"] += 1
    except Exception as e:
        err = getattr(e, "orig", e)          # the database's own error, inside SQLAlchemy's
        with lock:
            results[str(err.args) if err.args else repr(err)] += 1


print(f"{n} orders at once ...", flush=True)
start = time.time()
threads = [threading.Thread(target=buy, args=(seat,)) for seat in range(1, n + 1)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(f"placed: {results.pop('placed', 0)}")
for err, count in results.most_common():
    print(f"failed: {count}  {err}")
print(f"took {time.time() - start:.1f} s")
