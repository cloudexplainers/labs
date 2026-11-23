"""Capture Hillside Tractors' page as a real browser shows it (run by demo_driver.py:
python3 lab/capture.py <name> <port> <url shown in the address bar>)."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from browser_shots import Shots  # noqa: E402

name, port, url = sys.argv[1], sys.argv[2], sys.argv[3]
with Shots(HERE.parent) as s:
    s.page.set_default_navigation_timeout(60_000)
    s.page.goto(f"http://127.0.0.1:{port}/")
    s.page.wait_for_load_state("networkidle")
    if name == "server":                     # an unstyled page is 16 px text: zoom it the way a viewer's browser zoom would
        s.page.evaluate("document.body.style.zoom = '1.8'")
    boxes = {"title": "#title", "sub": "#sub", "logo": "#logo", "card1": "#card1"}
    if name != "server":
        boxes.update({"grid": "#grid", "card2": "#card2", "card3": "#card3"})
    s.shot(name, boxes=boxes, url=url)
print(f"shot {name}: {list(boxes)}")
