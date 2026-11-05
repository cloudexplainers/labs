"""The same total with NumPy: the numbers live in one block of plain 8-byte integers (best of 3)."""
import time
import numpy as np
N = 10_000_000
prices = np.arange(N, dtype=np.int64) % 50
best = 1e9
for _ in range(3):
    t = time.perf_counter()
    total = int(prices.sum())
    best = min(best, time.perf_counter() - t)
print(f"total:  {total:,} dollars")
print(f"numpy sum: {best:.4f} s")
