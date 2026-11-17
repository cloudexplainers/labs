"""The ice rink's booking website: today's skating sessions, read from the rink's database on every visit.

The connection address comes from DATABASE_URL (set in /etc/rink/rink.env), as most apps do. When the database
can't be reached, the page says so and shows the error psycopg2 gave, so the lab's browser capture shows it.
"""
import html
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import psycopg2

STYLE = """body{font-family:system-ui,sans-serif;margin:0;background:#eef4fa;color:#1d2a36}
header{background:#1f5f8b;color:#fff;padding:22px 40px;font-size:28px;font-weight:600}
main{padding:30px 40px}h1{font-size:26px;margin:0 0 18px}
table{border-collapse:collapse;background:#fff;min-width:640px}td,th{padding:12px 18px;border-bottom:1px solid #d5e0ea;text-align:left;font-size:20px}
.err{background:#fff;border-left:6px solid #c0392b;padding:18px 24px;max-width:900px}
.err h1{color:#c0392b}pre{white-space:pre-wrap;font-size:18px;background:#f6f8fa;padding:14px;margin:14px 0 0}"""


def page(body: str) -> bytes:
    return (f"<!doctype html><html><head><meta charset='utf-8'><title>Northside Ice Rink: bookings</title>"
            f"<style>{STYLE}</style></head><body><header>Northside Ice Rink</header><main>{body}</main>"
            f"</body></html>").encode()


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            conn = psycopg2.connect(os.environ["DATABASE_URL"], connect_timeout=10)
            with conn, conn.cursor() as cur:
                cur.execute("SELECT starts, name, places FROM sessions ORDER BY starts")
                rows = cur.fetchall()
            conn.close()
            cells = "".join(f"<tr><td>{s:%H:%M}</td><td>{html.escape(n)}</td><td>{p} places left</td></tr>"
                            for s, n, p in rows)
            body, code = (f"<h1>Today's skating sessions</h1><table><tr><th>Time</th><th>Session</th>"
                          f"<th>Free</th></tr>{cells}</table>"), 200
        except psycopg2.Error as e:
            body, code = (f"<div class='err'><h1>Bookings are unavailable right now</h1>"
                          f"<p>The booking site could not reach the rink's database.</p>"
                          f"<pre>{html.escape(str(e).strip())}</pre></div>"), 500
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(page(body))

    def log_message(self, fmt, *args):
        print(fmt % args, flush=True)


ThreadingHTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
