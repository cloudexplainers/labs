"""Prints what Claude Code did, from its stream-json output: whether the car-lot server
connected, each call to it with the arguments Claude chose, what came back, and the answer."""
import json
import sys
import textwrap


def say(prefix, text):
    for i, line in enumerate(textwrap.wrap(" ".join(str(text).split()), 70) or [""]):
        print((prefix if i == 0 else " " * len(prefix)) + line)


def short(result):
    try:
        data = json.loads(result)
    except (TypeError, ValueError):
        return result
    if isinstance(data, dict) and data.get("contents"):
        text = data["contents"][0].get("text", "")
        try:
            return json.dumps(json.loads(text), separators=(", ", ": "))
        except ValueError:
            return text
    cars = data.get("result") if isinstance(data, dict) else None
    if isinstance(cars, list):
        if not cars:
            return "no cars"
        return "; ".join(f'{c["stock"]} {c["year"]} {c["make"]} {c["model"]} ${int(c["price"]):,}'
                         for c in cars)
    return data.get("result", result) if isinstance(data, dict) else result


ours = set()   # ids of the calls to the car-lot server; Claude Code's own tools are not shown
for line in sys.stdin:
    try:
        ev = json.loads(line)
    except ValueError:
        continue
    if ev.get("type") == "system" and ev.get("subtype") == "init":
        for s in ev.get("mcp_servers", []):
            print(f'{s["name"]} server: {s["status"]}')
    elif ev.get("type") == "assistant":
        for part in ev["message"]["content"]:
            if part["type"] == "tool_use" and part["name"].startswith("mcp__"):
                ours.add(part["id"])
                args = " ".join(f"{k}={v}" for k, v in part["input"].items())
                say("-> ", f'{part["name"].split("__")[-1]} {args}')
            elif part["type"] == "tool_use" and part["name"] == "ReadMcpResourceTool":
                ours.add(part["id"])
                say("-> ", f'reads {part["input"]["uri"]}')
    elif ev.get("type") == "user":
        for part in ev["message"]["content"]:
            if isinstance(part, dict) and part.get("type") == "tool_result" and part.get("tool_use_id") in ours:
                body = part.get("content")
                if isinstance(body, list):
                    body = " ".join(b.get("text", "") for b in body if isinstance(b, dict))
                if part.get("is_error"):
                    say("<- error: ", body)
                elif body and str(body).strip():
                    say("<- ", short(body))
    elif ev.get("type") == "result":
        say("Claude: ", ev.get("result", ""))
