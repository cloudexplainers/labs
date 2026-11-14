"""Ana's Pottery Studio storefront app (runs behind Nginx on 127.0.0.1:8000 / 8002)."""
import json
import os

WORKER = os.environ.get("WORKER_NAME", "worker-1")

HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Riverbank Pottery Studio</title>
  <link rel="stylesheet" href="/static/studio.css">
</head>
<body>
  <main class="card">
    <h1 id="title">Riverbank Pottery Studio</h1>
    <p id="sub">Handmade stoneware &amp; open kiln hours · Served by {worker}</p>
    <table id="items">
      <thead><tr><th>Piece</th><th>Glaze</th><th>Price</th></tr></thead>
      <tbody>
        <tr id="row1"><td>Morning Mug</td><td>Speckled Oat</td><td>$34</td></tr>
        <tr><td>Pour-Over Dripper</td><td>River Slate</td><td>$48</td></tr>
        <tr><td>Serving Bowl</td><td>Warm Ash</td><td>$62</td></tr>
      </tbody>
    </table>
    <p class="foot"><a href="/kiln/">Book a Kiln Slot &rarr;</a></p>
  </main>
</body>
</html>
"""


def app(environ, start_response):
    path = environ.get("PATH_INFO", "/")
    if path == "/whoami":
        info = {
            "worker": WORKER,
            "host": environ.get("HTTP_HOST", "-"),
            "remote_addr": environ.get("REMOTE_ADDR", "-"),
            "x_real_ip": environ.get("HTTP_X_REAL_IP", "-"),
            "x_forwarded_for": environ.get("HTTP_X_FORWARDED_FOR", "-"),
            "x_forwarded_proto": environ.get("HTTP_X_FORWARDED_PROTO", "-"),
        }
        body = (json.dumps(info, indent=2) + "\n").encode()
        start_response("200 OK", [("Content-Type", "application/json"), ("Content-Length", str(len(body)))])
        return [body]

    if path == "/worker":
        body = f"{WORKER}\n".encode()
        start_response("200 OK", [("Content-Type", "text/plain"), ("Content-Length", str(len(body)))])
        return [body]

    if path == "/upload":
        length = int(environ.get("CONTENT_LENGTH") or 0)
        _ = environ["wsgi.input"].read(length)
        body = f"uploaded {length} bytes\n".encode()
        start_response("200 OK", [("Content-Type", "text/plain"), ("Content-Length", str(len(body)))])
        return [body]

    if path == "/":
        body = HTML.format(worker=WORKER).encode()
        start_response("200 OK", [("Content-Type", "text/html; charset=utf-8"), ("Content-Length", str(len(body)))])
        return [body]

    body = b"404 Not Found\n"
    start_response("404 Not Found", [("Content-Type", "text/plain"), ("Content-Length", str(len(body)))])
    return [body]
