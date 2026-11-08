"""Writes shop/catalog.txt: a made-up supplier catalog of 1,800 tea lots (about 100,000 tokens),
the kind of long document people paste into a chat. Same file every time (fixed seed)."""
import random

rng = random.Random(45)
teas = open("shop/teas.txt").read().splitlines()
regions = ["Shizuoka", "Kagoshima", "Uji", "Assam", "Darjeeling", "Fujian", "Yunnan", "Nilgiri", "Kenya", "Hunan"]
grades = ["first flush", "second flush", "autumnal", "spring picking", "summer picking"]
with open("shop/catalog.txt", "w") as f:
    f.write("Kettle Supply Co. wholesale catalog, lots on offer\n\n")
    for n in range(1, 1801):
        tea = rng.choice(teas)
        day = f"2026-{rng.randint(3, 10):02d}-{rng.randint(1, 28):02d}"
        f.write(f"Lot {n:04d}: {tea}, {rng.choice(regions)}, {rng.choice(grades)}, harvested {day}, "
                f"{rng.uniform(12, 90):.2f} dollars per kilo, {rng.randint(5, 400)} kilos available, "
                f"moisture {rng.uniform(3, 7):.1f} percent.\n")
