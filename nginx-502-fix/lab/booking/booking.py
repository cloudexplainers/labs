"""Crux Climbing's booking page (P127 lab): a tiny WSGI app run by gunicorn behind nginx.

/         the week's sessions, read from sessions.csv
/report   the month's report: slow on purpose (REPORT_SECONDS), like a big database query
/login    signs a member in; its session cookie carries their saved bookings, so it is large
"""
import csv
import os
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPORT_SECONDS = 75

PAGE = """<!doctype html><html><head><meta charset="utf-8"><title>Crux Climbing: book a session</title>
<style>body{{font:22px system-ui,sans-serif;margin:40px 60px;background:#f6f4ef;color:#222}}
h1{{font-size:40px;margin:0 0 6px}}p{{color:#555;margin:0 0 26px}}table{{border-collapse:collapse;width:100%}}
th,td{{text-align:left;padding:12px 16px;border-bottom:1px solid #ddd}}th{{background:#e8e2d4}}
td.free{{color:#1d7a3a;font-weight:600}}</style></head><body>
<h1 id="title">Crux Climbing</h1><p id="sub">Book a session at the wall. Served by gunicorn, behind nginx.</p>
<table id="sessions"><tr><th>Day</th><th>Time</th><th>Session</th><th>Places left</th></tr>{rows}</table>
</body></html>"""


def sessions():
    with open(HERE / "sessions.csv", newline="") as f:
        return list(csv.DictReader(f))


def app(environ, start_response):
    path = environ.get("PATH_INFO", "/")
    if path == "/report":
        time.sleep(REPORT_SECONDS)
        body = f"Monthly report: {len(sessions()) * 31} bookings\n".encode()
        start_response("200 OK", [("Content-Type", "text/plain"), ("Content-Length", str(len(body)))])
        return [body]
    if path == "/login":
        saved = ";".join(f"{s['day']}-{s['time']}-{s['session']}" for s in sessions() * 40)
        body = b"Signed in\n"
        start_response("200 OK", [("Content-Type", "text/plain"), ("Content-Length", str(len(body))),
                                  ("Set-Cookie", f"crux_session={saved.replace(' ', '_')}; Path=/; HttpOnly")])
        return [body]
    rows = "".join(f'<tr id="row{i + 1}"><td>{s["day"]}</td><td>{s["time"]}</td><td>{s["session"]}</td>'
                   f'<td class="free">{s["places"]}</td></tr>' for i, s in enumerate(sessions()))
    body = PAGE.format(rows=rows).encode()
    start_response("200 OK", [("Content-Type", "text/html; charset=utf-8"), ("Content-Length", str(len(body)))])
    return [body]
