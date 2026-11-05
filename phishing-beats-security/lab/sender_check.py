"""Split a From line into the name you see and the address it really came from."""
import sys
from email.utils import parseaddr

SAVED = "bank.example"

name, address = parseaddr(sys.argv[1])
domain = address.rsplit("@", 1)[-1]
print(f"name shown:   {name}")
print(f"real address: {address}")
print("from your bank?", "YES" if domain == SAVED else "NO")
