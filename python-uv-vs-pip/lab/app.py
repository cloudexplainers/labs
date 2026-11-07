import pandas as pd
import requests

prices = requests.get("http://localhost:8000/prices.json", timeout=5).json()
menu = pd.Series(prices, name="price")
print(menu.to_string())
print(f"average: ${menu.mean():.2f}")
