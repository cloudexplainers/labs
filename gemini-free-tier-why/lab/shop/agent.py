import httpx
from google import genai
from google.genai import types

sent = []   # every request the library sends to the API
web = httpx.Client(event_hooks={"request": [sent.append]})
client = genai.Client(
    http_options=types.HttpOptions(httpx_client=web))

def teas() -> list[str]:
    """The names of every tea the shop sells."""
    return open("teas.txt").read().splitlines()

def stock(tea: str) -> int:
    """How many tins of one tea are in stock."""
    return {"Matcha": 0, "Gyokuro": 0}.get(tea, 12)

try:
    reply = client.models.generate_content(model="gemini-3.6-flash",
        contents="Which of our teas are out of stock?",
        config=types.GenerateContentConfig(tools=[teas, stock]))
    print(reply.text)
finally:
    print("requests sent:", len(sent))
