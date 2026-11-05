"""Read the real address of a link, the way your browser does. Test domains only (RFC 2606/6761)."""
import sys
from urllib.parse import urlsplit

SAVED = "bank.example"          # the site you actually use

url = sys.argv[1]
host = urlsplit(url).hostname   # after //, before the next /, ignoring anything before @
owner = ".".join(host.split(".")[-2:])  # read right to left: the last two parts own it
print(f"host:  {host}")
print(f"owner: {owner}")
print("your bank?", "YES" if owner == SAVED else "NO")
