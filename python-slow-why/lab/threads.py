"""CPU-heavy work (counting) split across 4 threads, then 4 processes."""
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
def count(n):
    s = 0
    for i in range(n):
        s += i
    return s
WORK = 20_000_000
def timed(label, fn):
    t = time.perf_counter(); fn(); print(f"{label:<12} {time.perf_counter() - t:.2f} s")
timed("1 thread:", lambda: count(WORK))
with ThreadPoolExecutor(4) as ex:
    timed("4 threads:", lambda: list(ex.map(count, [WORK // 4] * 4)))
with ProcessPoolExecutor(4) as ex:
    list(ex.map(count, [1] * 4))   # start the 4 processes first
    timed("4 processes:", lambda: list(ex.map(count, [WORK // 4] * 4)))
