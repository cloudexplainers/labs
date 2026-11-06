import re
from pathlib import Path

from pypdf import PdfReader, PdfWriter

shop = Path.home() / "shop"


def run():
    merged = PdfWriter()
    owed = 0.0
    for path in sorted((shop / "invoices").glob("invoice-*.pdf")):
        text = PdfReader(path).pages[0].extract_text()
        due = float(re.search(r"Total due: \$([\d.]+)", text).group(1))
        print(f"{path.name}: ${due:.2f}")
        owed += due
        merged.append(path)

    merged.write(shop / "invoices-all.pdf")
    print(f"Owed to Highland Leaf: ${owed:.2f} (merged into invoices-all.pdf)")


if __name__ == "__main__":
    run()
