"""Add up 10 million order totals with a plain Python loop (best of 3 runs)."""
import time
N = 10_000_000
prices = [i % 50 for i in range(N)]          # one price per order, 0-49 dollars
best = 1e9
for _ in range(3):
    t = time.perf_counter()
    total = 0
    for p in prices:
        total += p
    best = min(best, time.perf_counter() - t)
print(f"orders: {N:,}")
print(f"total:  {total:,} dollars")
print(f"python loop: {best:.3f} s")
