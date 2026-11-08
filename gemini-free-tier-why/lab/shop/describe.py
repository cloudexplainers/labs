import json, time
from google import genai

client = genai.Client()
for n, tea in enumerate(open("teas.txt").read().splitlines(), 1):
    while True:
        try:
            client.models.generate_content(model="gemini-3.6-flash",
                contents=f"Two calm sentences for a shop page about {tea} tea.")
            break
        except genai.errors.ServerError as e:   # 503: the model is busy
            print(n, tea, f"busy ({e.code}), trying again")
            time.sleep(30)
        except genai.errors.ClientError as e:   # 4xx, like 429: stop here
            json.dump(e.details, open("error.json", "w"))
            exit(f"{n} {tea}: error {e.code} {e.status}")
    print(n, tea, "done")
    time.sleep(13)   # 5 requests a minute is the limit
