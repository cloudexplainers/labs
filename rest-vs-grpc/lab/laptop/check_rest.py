# Ana's order service asks the stock service over REST: a plain HTTP GET that answers JSON.
import httpx

tea = httpx.get("http://stock:8000/teas/sencha").json()
print(f"{tea['name']}: {tea['stock']} in stock")
