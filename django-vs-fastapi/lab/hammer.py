"""Send N requests at the same moment and time how long until the last answer arrives."""
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

url, n = "http://" + sys.argv[1], int(sys.argv[2])


def get(_):
    with urllib.request.urlopen(url, timeout=300) as r:
        return r.status


start = time.time()
with ThreadPoolExecutor(n) as pool:
    codes = list(pool.map(get, range(n)))
print(f"{codes.count(200)} of {n} requests answered in {time.time() - start:.1f} seconds")
