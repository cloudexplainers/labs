"""Sarah's yard screen: asks the tracker which cars stand on which track."""
import json
import urllib.request

with urllib.request.urlopen("http://tracker:8080/cars", timeout=10) as r:
    for track, cars in json.load(r).items():
        print(f"{track}: {cars} cars")
