"""Makes six stand-in recipe photos (plain colour gradients) for the lab, at image build time."""
import sys
from pathlib import Path

from PIL import Image

out = Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)
names = ["grandmas-lasagna", "sunday-pancakes", "aunt-roses-chili", "lemon-bars", "chicken-soup", "apple-crumble"]
for i, n in enumerate(names):
    img = Image.new("RGB", (1600, 1200))
    img.putdata([((40 * i + x // 8) % 256, (y // 6) % 256, 120) for y in range(1200) for x in range(1600)])
    img.save(out / f"{n}.jpg", quality=80)
