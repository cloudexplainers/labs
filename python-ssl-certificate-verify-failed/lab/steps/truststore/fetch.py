import truststore
truststore.inject_into_ssl()
import sys

import requests

url = sys.argv[1]
check = "--no-verify" not in sys.argv
r = requests.get(url, timeout=10, verify=check)
print(r.status_code, r.reason)
