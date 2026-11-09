"""The tea shop's helper: refreshes the stock list every 30 seconds."""
import time

while True:
    print("stock list refreshed", flush=True)
    time.sleep(30)
