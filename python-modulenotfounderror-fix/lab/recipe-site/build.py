#!/usr/bin/python3
"""Builds the family recipe site: one web page for each recipe in recipes/."""
import sys
from pathlib import Path

import yaml

from family.render import page, slug

out = Path(sys.argv[1] if len(sys.argv) > 1 else "public")
out.mkdir(exist_ok=True)
recipes = sorted(Path("recipes").glob("*.yaml"))
for f in recipes:
    recipe = yaml.safe_load(f.read_text())
    (out / f"{slug(recipe['name'])}.html").write_text(page(recipe))
print(f"Built {len(recipes)} recipe pages in {out}/")
