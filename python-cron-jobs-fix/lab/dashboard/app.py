"""The bike rental shop's dashboard for the lab: one page that lists the reports received today, and one address a script posts
the report to. A report needs the shop's key in the X-API-Key header. Standard library only."""
import html
import json
import os
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

KEY = os.environ["BIKES_API_KEY"]
STATE = "/var/lib/dashboard/latest.json"

PAGE = """<!doctype html><html><head><meta charset="utf-8"><title>City Bikes dashboard</title><style>
body{{font-family:system-ui,sans-serif;margin:0;background:#f4f5f7;color:#1c2330}}
header{{background:#16324f;color:#fff;padding:20px 60px;font-size:30px;font-weight:600}}
main{{max-width:1400px;margin:30px auto;padding:0 60px}}
h1{{font-size:52px;margin:0 0 4px}} .day{{color:#5b6677;font-size:28px;margin-bottom:24px}}
.card{{background:#fff;border-radius:18px;padding:34px 48px 40px;box-shadow:0 2px 10px rgba(0,0,0,.08)}}
.label{{font-size:26px;color:#5b6677;text-transform:uppercase;letter-spacing:.06em}}
.status{{font-size:76px;font-weight:700;margin:10px 0 2px;display:inline-block}} .none{{color:#b3261e}} .ok{{color:#1b7f3b}}
.detail{{font-size:32px;color:#3a4454}} table{{border-collapse:collapse;margin-top:26px;font-size:44px}}
td{{padding:14px 70px 14px 14px}} td.n{{font-weight:700}} tr{{border-top:2px solid #e3e6ea}}
</style></head><body><header>City Bikes &middot; rental dashboard</header><main>
<h1>Daily report</h1><div class="day" id="day">{day}</div>
<div class="card"><div class="label">Reports received today</div>{body}</div></main></body></html>"""


def today():
    return time.strftime("%Y-%m-%d", time.gmtime())


def load():
    try:
        return [r for r in json.load(open(STATE)) if r["day"] == today()]
    except (OSError, ValueError):
        return []


def body():
    rows = load()
    if not rows:
        return ('<div class="status none" id="status">None yet</div>'
                '<div class="detail" id="detail">The report script has not sent anything today.</div>')
    trs = "".join(f'<tr id="row{i + 1}"><td class="n">{html.escape(r["at"])} UTC</td><td>{r["rentals"]} rentals</td>'
                  f'<td>${r["takings"]:.2f}</td></tr>' for i, r in enumerate(rows))
    return (f'<div><span class="status ok" id="status">{len(rows)} received</span></div>'
            f'<div><span class="detail" id="detail">Last one at {html.escape(rows[-1]["at"])} UTC</span></div>'
            f'<table id="rows">{trs}</table>')


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def send(self, code, text, kind="text/plain"):
        data = text.encode()
        self.send_response(code)
        self.send_header("Content-Type", kind + "; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/":
            self.send(200, PAGE.format(day=time.strftime("%A, %d %B %Y", time.gmtime()), body=body()), "text/html")
        else:
            self.send(404, "not found\n")

    def do_POST(self):
        if self.path != "/daily":
            return self.send(404, "not found\n")
        if self.headers.get("X-API-Key") != KEY:
            return self.send(401, "wrong or missing key\n")
        r = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
        now = time.gmtime()
        rows = load() + [{"day": today(), "at": time.strftime("%H:%M:%S", now), "rentals": int(r["rentals"]),
                          "takings": float(r["takings"])}]
        json.dump(rows, open(STATE, "w"))
        self.send(200, "ok\n")


ThreadingHTTPServer(("0.0.0.0", 8000), H).serve_forever()
