"""Capture Crux Climbing's page as a real browser shows it (run by demo_driver.py: python3 lab/capture.py <name> [path])."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from browser_shots import Shots  # noqa: E402

name = sys.argv[1]
path = sys.argv[2] if len(sys.argv) > 2 else "/"
with Shots(HERE.parent) as s:
    s.page.set_default_navigation_timeout(120_000)
    s.page.goto(f"http://127.0.0.1:18127{path}")
    if s.page.locator("#sessions").count():
        boxes = {"title": "#title", "sub": "#sub", "table": "#sessions", "row1": "#row1"}
    else:                                    # nginx's own error page: <center><h1>502 Bad Gateway</h1></center><hr><center>nginx/…
        boxes = {"code": "h1", "server": "hr + center"}
        # nginx's own error page is unstyled 16 px text: zoom it the way a viewer's browser zoom would (250%)
        s.page.evaluate("document.body.style.zoom = '2.5'")
    s.shot(name, boxes=boxes, url=f"http://crux.lab{path}")
print(f"shot {name}: {list(boxes)}")
