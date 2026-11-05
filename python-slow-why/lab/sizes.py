"""What one number costs in Python: every int is a full object."""
import sys
n = 42
print(f"value:          {n}")
print(f"type:           {type(n).__name__}")
print(f"size in memory: {sys.getsizeof(n)} bytes")
print("same number in C (long long): 8 bytes")
