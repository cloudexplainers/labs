"""Make Ana's messy Downloads folder for P092 (run off-screen, as root, before the demo).

Daily order exports from her online shop (CSV) and invoices from her tea supplier (PDF), plus two files that have
nothing to do with either. Everything is made up and fixed by a seed, so every run makes the same files.
The PDFs are written by hand (one page of Helvetica text each), so no PDF library is needed here: Ana's project
installs pypdf on camera to read them.
"""
import csv
import datetime as dt
import os
import random
import sys
from pathlib import Path

home = Path(sys.argv[1] if len(sys.argv) > 1 else "/home/ana")
down = home / "Downloads"
down.mkdir(parents=True, exist_ok=True)
rng = random.Random(92)

TEAS = {"Earl Grey": 6.50, "Sencha": 7.25, "Darjeeling": 8.00, "Rooibos": 5.75, "Jasmine Pearls": 9.50,
        "Masala Chai": 6.00}
WEIGHT = [5, 3, 2, 3, 1, 3]

day, n = dt.date(2026, 9, 21), 1000
while day <= dt.date(2026, 11, 5):
    if day.weekday() < 5 and rng.random() < 0.8:
        rows = []
        for _ in range(rng.randint(6, 14)):
            n += 1
            tea = rng.choices(list(TEAS), WEIGHT)[0]
            qty = rng.choice([1, 1, 1, 2, 2, 3])
            rows.append({"order_id": f"A-{n}", "date": day.isoformat(), "tea": tea, "qty": qty,
                         "price": f"{TEAS[tea] * qty:.2f}"})
        with open(down / f"orders-{day.isoformat()}.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
    day += dt.timedelta(days=1)


def pdf(path: Path, lines: list[str]) -> None:
    """A one-page PDF with these lines of text (Helvetica 12 pt), objects and xref written by hand."""
    def esc(s: str) -> str:
        return s.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    ops = ["BT", "/F1 12 Tf", "16 TL", "72 760 Td"] + [f"({esc(l)}) Tj T*" for l in lines] + ["ET"]
    stream = "\n".join(ops).encode("latin-1")
    objs = [b"<< /Type /Catalog /Pages 2 0 R >>",
            b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R "
            b"/Resources << /Font << /F1 5 0 R >> >> >>",
            b"<< /Length %d >>\nstream\n" % len(stream) + stream + b"\nendstream",
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"]
    out, offsets = bytearray(b"%PDF-1.4\n"), []
    for i, o in enumerate(objs, 1):
        offsets.append(len(out))
        out += b"%d 0 obj\n" % i + o + b"\nendobj\n"
    xref = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1)
    out += b"".join(b"%010d 00000 n \n" % o for o in offsets)
    out += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objs) + 1, xref)
    path.write_bytes(out)


INVOICES = [("HL-1042", "2026-10-06", [("Earl Grey, 5 kg", 140.00), ("Sencha, 3 kg", 117.00)]),
            ("HL-1057", "2026-10-20", [("Darjeeling, 2 kg", 104.00), ("Rooibos, 4 kg", 88.00),
                                       ("Jasmine Pearls, 1 kg", 61.50)]),
            ("HL-1063", "2026-11-03", [("Earl Grey, 5 kg", 140.00), ("Masala Chai, 3 kg", 79.50)])]
for num, date, items in INVOICES:
    total = sum(p for _, p in items)
    pdf(down / f"invoice-{num}.pdf",
        ["Highland Leaf Co. - wholesale tea", "", f"Invoice {num}", f"Date: {date}", "Bill to: Ana's Tea Shop", ""]
        + [f"{name}    ${price:.2f}" for name, price in items]
        + ["", f"Total due: ${total:.2f}", "Payment within 30 days."])

(down / "tea-label-draft.png").write_bytes(b"\x89PNG\r\n\x1a\n" + bytes(64))
(down / "notes.txt").write_text("call Highland Leaf about the chai order\n")
for p in down.iterdir():
    t = dt.datetime(2026, 11, 5, 18, 0).timestamp()
    os.utime(p, (t, t))
print(f"{sum(1 for _ in down.iterdir())} files in {down}")
