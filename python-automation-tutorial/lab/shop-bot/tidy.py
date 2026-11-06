from pathlib import Path

downloads = Path.home() / "Downloads"
shop = Path.home() / "shop"


def move(file, folder):
    folder.mkdir(parents=True, exist_ok=True)  # make it if it's missing
    file.rename(folder / file.name)


def run():
    orders = sorted(downloads.glob("orders-*.csv"))
    for file in orders:
        month = file.name[7:14]  # orders-2026-10-03.csv -> 2026-10
        move(file, shop / "orders" / month)

    invoices = sorted(downloads.glob("invoice-*.pdf"))
    for file in invoices:
        move(file, shop / "invoices")

    print(f"Moved {len(orders)} order files and {len(invoices)} invoices")


if __name__ == "__main__":
    run()
