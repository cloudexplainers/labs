import httpx

r = httpx.get("http://shop.test/api/teas")
r.raise_for_status()
teas = r.json()
print("Teas found:", len(teas))
for tea in teas[:3]:
    print(f"{tea['name']}: {tea['price']} EUR")
