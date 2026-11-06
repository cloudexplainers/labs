"""Ana's own script: asks the Anthropic API for one line, using the key in ANTHROPIC_API_KEY.
Standard library only, so it runs anywhere with Python 3."""
import json
import os
import urllib.error
import urllib.request

key = os.environ.get("ANTHROPIC_API_KEY")
if not key:
    raise SystemExit("app.py: no ANTHROPIC_API_KEY for this program")
req = urllib.request.Request(
    "https://api.anthropic.com/v1/messages",
    data=json.dumps({"model": "claude-haiku-5-5", "max_tokens": 50,
                     "messages": [{"role": "user", "content": "One line about green tea."}]}).encode(),
    headers={"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"})
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        print("API answered:", json.load(r)["content"][0]["text"])
except urllib.error.HTTPError as e:
    err = json.load(e)["error"]
    print(f"API answered: {e.code} {err['type']}: {err['message']}")
