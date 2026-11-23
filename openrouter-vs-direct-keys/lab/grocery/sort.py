"""Kari's grocery list app: sorts list.txt by store aisle with an AI model.
python sort.py google   (Google's own key)   |   python sort.py router   (OpenRouter's key)
The door's settings come from google.env or router.env; MODEL=... on the command line picks another model,
and MODEL=a,b (OpenRouter only) sends a list: if the first model fails, OpenRouter tries the next."""
import os
import re
import sys

from openai import OpenAI, APIStatusError, APIConnectionError

door = sys.argv[1]
cfg = dict(l.strip().split("=", 1) for l in open(f"{door}.env") if "=" in l)
models = (os.environ.get("MODEL") or cfg["MODEL"]).split(",")
extra = {"models": models} if len(models) > 1 else {}
client = OpenAI(base_url=cfg["BASE_URL"], api_key=os.environ[cfg["KEY"]], max_retries=0, timeout=120)
groceries = open("list.txt").read().strip()
try:
    reply = client.chat.completions.create(model=models[0], extra_body=extra, max_tokens=2000, messages=[
        {"role": "system", "content": "You sort grocery lists by store aisle. Reply with one line per aisle, "
                                      "like 'Produce: apples, bananas'. No other text."},
        {"role": "user", "content": groceries}])
except APIStatusError as e:
    body = e.body[0] if isinstance(e.body, list) and e.body else e.body   # Google answers with a list
    err = body.get("error", body) if isinstance(body, dict) else {}
    meta = err.get("metadata") or {}
    msg = meta.get("raw") or err.get("message") or str(e)
    print(f"error {e.status_code}: {msg.split(': https')[0].split(' Manage it')[0]}")
    if meta.get("provider_name"):
        print(f"provider:     {meta['provider_name']}")
    if meta.get("limit_source"):
        print(f"limit source: {meta['limit_source']}")
    sys.exit(1)
except APIConnectionError as e:
    print(f"error: no answer ({e.__class__.__name__})")
    sys.exit(1)
text = re.sub(r"(?s)<thought>.*?</thought>", "", reply.choices[0].message.content or "").strip()
print(text)
print()
print(f"model:        {reply.model}")
print(f"sent to:      {cfg['BASE_URL'].split('/')[2]}")
if getattr(reply, "provider", None):
    print(f"run by:       {reply.provider}")
