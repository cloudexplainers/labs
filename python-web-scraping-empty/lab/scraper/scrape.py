import requests
from bs4 import BeautifulSoup

page = requests.get("http://shop.test/")
print("Status:", page.status_code)

soup = BeautifulSoup(page.text, "html.parser")
teas = soup.select("li.tea")
print("Teas found:", len(teas))
