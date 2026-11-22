"""Jen's script: a small photo for each recipe page."""
from pathlib import Path

from PIL import Image

from family.render import slug

out = Path("public/thumbs")
out.mkdir(parents=True, exist_ok=True)
photos = sorted(Path("photos").glob("*.jpg"))
for p in photos:
    img = Image.open(p)
    img.thumbnail((320, 320))
    img.save(out / f"{slug(p.stem.replace('-', ' '))}.jpg")
print(f"Made {len(photos)} thumbnails in {out}/")
