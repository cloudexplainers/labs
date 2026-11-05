"""The same total with Python's built-in sum(), which loops in C (best of 3)."""
import time
N = 10_000_000
prices = [i % 50 for i in range(N)]
best = 1e9
for _ in range(3):
    t = time.perf_counter()
    total = sum(prices)
    best = min(best, time.perf_counter() - t)
print(f"total:  {total:,} dollars")
print(f"built-in sum(): {best:.3f} s")
