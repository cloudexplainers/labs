import time
import httpx

headers = {"User-Agent": "tea-price-bot (ana@example.com)"}
with httpx.Client(headers=headers) as client:
    for n in range(1, 9):
        r = client.get(f"http://shop.test/api/teas/{n}")
        if r.status_code == 429:
            time.sleep(int(r.headers["Retry-After"]))
            r = client.get(f"http://shop.test/api/teas/{n}")
        print(n, r.status_code, r.json()["name"])
        time.sleep(1)  # the shop's crawl delay
