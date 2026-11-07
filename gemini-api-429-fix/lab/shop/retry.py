import random
import time
from google import genai
from google.genai import errors

client = genai.Client()  # finds the key in GEMINI_API_KEY
teas = open("teas.txt").read().splitlines()


def wait_time(e):
    """How long the API asked us to wait (its RetryInfo), else 10 seconds."""
    for detail in e.details["error"]["details"]:
        if detail["@type"].endswith("RetryInfo"):
            return float(detail["retryDelay"].rstrip("s"))
    return 10


def describe(tea):
    for attempt in range(5):
        try:
            return client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=f"One calm sentence about {tea} tea for our shop page.",
            )
        except errors.ClientError as e:
            if e.code != 429 or "PerDay" in str(e):
                raise  # not a short wait: stop and read the error
            wait = wait_time(e) + random.uniform(0, 1)  # plus jitter
            print(f"   429: waiting {wait:.0f} s")
            time.sleep(wait)
    raise SystemExit("still 429 after 5 tries")


for n, tea in enumerate(teas, 1):
    describe(tea)
    print(n, tea, "done")
