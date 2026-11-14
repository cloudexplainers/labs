"""Capture Riverbank Pottery Studio pages in a real browser (run by demo_driver.py)."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from browser_shots import Shots  # noqa: E402

name = sys.argv[1]
path = sys.argv[2] if len(sys.argv) > 2 else "/"
url_label = sys.argv[3] if len(sys.argv) > 3 else f"http://shop.pottery.test{path}"

with Shots(HERE.parent) as s:
    s.page.set_default_navigation_timeout(60_000)
    s.page.goto(f"http://127.0.0.1:18146{path}")
    if s.page.locator("#items").count():
        boxes = {"title": "#title", "sub": "#sub", "table": "#items", "row1": "#row1"}
    elif s.page.locator("#firings").count():
        boxes = {"title": "#title", "sub": "#sub", "table": "#firings", "row1": "#row1"}
    else:
        boxes = {"title": "h1"}
    s.shot(name, boxes=boxes, url=url_label)
print(f"shot {name}: {list(boxes)}")
