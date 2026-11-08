# Ben's price checker: reads the tea shop's prices over HTTPS, with Python's requests library.
import re

import requests

try:
    r = requests.get("https://shop.test/prices.json", timeout=10)
    print(r.status_code, r.json())
except requests.exceptions.SSLError as e:
    reason = re.search(r"\[SSL: .*?\(_ssl\.c:\d+\)", str(e))
    print("SSLError:", reason.group(0) if reason else e)
