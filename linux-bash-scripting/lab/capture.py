"""Captures P102's browser shots with a real Chromium (run on the Mac after demo.sh):

    /opt/homebrew/bin/python3.14 remotion_shorts/videos/linux-bash-scripting/lab/capture.py

1. report.html, the page Ana's finished script wrote inside the lab container (demo.sh copies it and its
   stylesheet out to lab_out/). It is served from that folder on localhost; the address shown is the file's own
   place on the station box.
2. ShellCheck's public wiki page for SC2086, the warning the tool printed in the demo.
"""
import functools
import http.server
import sys
import threading
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from browser_shots import Shots  # noqa: E402


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


handler = functools.partial(Quiet, directory=str(HERE.parent / "lab_out"))
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
threading.Thread(target=srv.serve_forever, daemon=True).start()
base = f"http://127.0.0.1:{srv.server_port}"

with Shots(HERE.parent) as s:
    s.page.goto(base + "/report.html", wait_until="networkidle")
    s.shot("report", url="file:///home/ana/report.html", boxes={
        "title": "h1", "sub": "p.sub", "table": "table",
        "garden": "tr:nth-child(2)", "north": "tr:nth-child(3)", "roof": "tr:nth-child(4)",
        "missing": "td.missing", "count": "tr:nth-child(3) td:nth-child(2)"})
    s.page.goto("https://www.shellcheck.net/wiki/SC2086", wait_until="networkidle")
    s.shot("sc2086", boxes={"heading": "h1 >> nth=0", "problem": "pre >> nth=0", "fix": "pre >> nth=1"})
srv.shutdown()
print("shots saved")
