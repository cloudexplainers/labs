import os
import httpx
from google import genai
from google.genai import types
from pydantic import BaseModel

class Page(BaseModel):
    tea: str
    text: str

sent = []   # every request the library sends to the API
web = httpx.Client(event_hooks={"request": [sent.append]})
client = genai.Client(
    http_options=types.HttpOptions(httpx_client=web))
teas = open("teas.txt").read()
model = os.environ.get("MODEL", "gemini-3.6-flash")
prompt = "For each tea, two calm sentences for a shop page.\n" + teas
config = types.GenerateContentConfig(
    response_mime_type="application/json", response_schema=list[Page])
reply = client.models.generate_content(
    model=model, contents=prompt, config=config)
pages = reply.parsed
print(len(pages), "descriptions. The first:", pages[0].tea, "-",
      pages[0].text[:40], "...")
print("requests sent:", len(sent))
