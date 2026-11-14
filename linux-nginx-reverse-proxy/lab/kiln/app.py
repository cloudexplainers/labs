"""Ana's Kiln Booking app (runs behind Nginx on 127.0.0.1:8001)."""

HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Kiln Schedule · Riverbank Pottery</title>
  <link rel="stylesheet" href="/static/studio.css">
</head>
<body>
  <main class="card">
    <h1 id="title">Kiln Firing Schedule</h1>
    <p id="sub">Cone 6 Electric Kiln · Reserve a shelf before Friday</p>
    <table id="firings">
      <thead><tr><th>Day</th><th>Cycle</th><th>Status</th></tr></thead>
      <tbody>
        <tr id="row1"><td>Tuesday</td><td>Bisque 06</td><td>Open (4 shelves)</td></tr>
        <tr><td>Thursday</td><td>Glaze Cone 6</td><td>Open (2 shelves)</td></tr>
        <tr><td>Saturday</td><td>Glaze Cone 6</td><td>Full</td></tr>
      </tbody>
    </table>
    <p class="foot"><a href="/">&larr; Back to Storefront</a></p>
  </main>
</body>
</html>
"""


def app(environ, start_response):
    path = environ.get("PATH_INFO", "/")
    if path == "/":
        body = HTML.encode()
        start_response("200 OK", [("Content-Type", "text/html; charset=utf-8"), ("Content-Length", str(len(body)))])
        return [body]

    body = f"404 Not Found: {path}\n".encode()
    start_response("404 Not Found", [("Content-Type", "text/plain"), ("Content-Length", str(len(body)))])
    return [body]
