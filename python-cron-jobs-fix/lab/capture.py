"""Capture the lab dashboard as a real browser renders it (run by demo_driver.py: python3 lab/capture.py <name>)."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from browser_shots import Shots  # noqa: E402

name = sys.argv[1]
boxes = {"title": "h1", "day": "#day", "status": "#status", "detail": "#detail"}
with Shots(HERE.parent) as s:
    s.page.goto("http://127.0.0.1:18093/")
    n = s.page.locator("#rows tr").count()
    for i in range(n):
        boxes[f"row{i + 1}"] = f"#row{i + 1}"
    s.shot(name, boxes=boxes, url="http://localhost:8000/")
print(f"shot {name}: {n} rows")
