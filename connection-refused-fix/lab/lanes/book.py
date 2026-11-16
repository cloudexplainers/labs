# The front desk's booking screen: asks the lanes server which lanes are free.
import json
import urllib.request

with urllib.request.urlopen("http://lanes:5000/lanes", timeout=10) as answer:
    print("Free lanes:", *json.load(answer)["free"])
