"""A tiny tea shop for the scraping lab (P091). Python's standard library only.

/            the page: an empty list and a script tag; the browser's JavaScript fills the list
/app.js      fetches /api/teas and draws one <li class="tea"> per tea
/api/teas    the tea list as JSON (it takes 0.3 seconds, like a real database query)
/api/teas/N  one tea
/robots.txt  the shop's rules for bots
More than 5 requests in one second from one address get 429 Too Many Requests, with Retry-After.
Every request is logged to /var/log/shop.log: method, path, status and the client's User-Agent.
"""
import json
import time
from collections import defaultdict, deque
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

TEAS = [
    ("Sencha", 8.0), ("Jasmine Pearls", 12.5), ("Earl Grey", 6.0), ("Darjeeling", 9.5),
    ("Genmaicha", 7.0), ("Oolong", 11.0), ("Assam", 5.5), ("Rooibos", 6.5),
    ("Matcha", 18.0), ("Chamomile", 4.5), ("Lapsang Souchong", 10.0), ("Peppermint", 4.0),
]
TEAS = [{"id": i + 1, "name": n, "price": p} for i, (n, p) in enumerate(TEAS)]

PAGE = """<!doctype html>
<html>
<head><title>Ana's Tea Shop</title></head>
<body>
  <h1>Our teas</h1>
  <ul id="teas"></ul>
  <script src="/app.js"></script>
</body>
</html>
"""

APP = """fetch("/api/teas")
  .then(r => r.json())
  .then(teas => {
    const list = document.getElementById("teas");
    for (const t of teas) {
      const li = document.createElement("li");
      li.className = "tea";
      li.textContent = `${t.name}: ${t.price} EUR`;
      list.append(li);
    }
  });
"""

ROBOTS = """User-agent: *
Disallow: /account/
Crawl-delay: 1
"""

WINDOW, LIMIT = 1.0, 5
seen = defaultdict(deque)


class Shop(BaseHTTPRequestHandler):
    server_version = "TeaShop/1.0"
    sys_version = ""

    def send(self, status, body, ctype, extra=()):
        data = body.encode()
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        for k, v in extra:
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(data)
        with open("/var/log/shop.log", "a") as log:
            agent = self.headers.get("User-Agent", "-")
            log.write(f"{self.command} {self.path} {status} {agent}\n")

    def do_GET(self):
        now, q = time.monotonic(), seen[self.client_address[0]]
        while q and now - q[0] > WINDOW:
            q.popleft()
        q.append(now)
        if len(q) > LIMIT:
            return self.send(429, "Too Many Requests\n", "text/plain", [("Retry-After", "2")])
        path = self.path
        if path == "/":
            return self.send(200, PAGE, "text/html; charset=utf-8")
        if path == "/app.js":
            return self.send(200, APP, "text/javascript")
        if path == "/robots.txt":
            return self.send(200, ROBOTS, "text/plain")
        if path == "/api/teas":
            time.sleep(0.3)
            return self.send(200, json.dumps(TEAS), "application/json")
        if path.startswith("/api/teas/") and path[10:].isdigit() and 1 <= int(path[10:]) <= len(TEAS):
            return self.send(200, json.dumps(TEAS[int(path[10:]) - 1]), "application/json")
        return self.send(404, "Not Found\n", "text/plain")

    def log_message(self, *a):
        pass


ThreadingHTTPServer(("0.0.0.0", 80), Shop).serve_forever()
