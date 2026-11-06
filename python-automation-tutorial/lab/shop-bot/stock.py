import os

import httpx

URL = "http://localhost:8000/api/stock"


def run():
    key = os.environ.get("SUPPLIER_KEY", "")
    response = httpx.get(URL, headers={"X-API-Key": key}, timeout=10)
    response.raise_for_status()  # stop here on 401, 404, 500...

    for item in response.json():
        if item["kg"] < 10:
            print(f"Low at Highland Leaf: {item['tea']}, {item['kg']} kg left")


if __name__ == "__main__":
    run()
