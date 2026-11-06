import httpx

for n in range(1, 9):
    r = httpx.get(f"http://shop.test/api/teas/{n}")
    print(n, r.status_code)
