import csv

from openpyxl import Workbook


def read_orders(path):
    with open(path) as f:
        return list(csv.DictReader(f))


def totals(orders):
    sold = {}
    for row in orders:
        item = row["item"]
        sold[item] = sold.get(item, 0) + int(row["qty"])
    return sold


def revenue(orders):
    money = {}
    for row in orders:
        item = row["item"]
        money[item] = money.get(item, 0) + int(row["qty"]) * float(row["price"])
    return money


def save_report(orders, path):
    book = Workbook()
    sheet = book.active
    sheet.append(["item", "sold", "revenue"])
    sold, money = totals(orders), revenue(orders)
    for item in sold:
        sheet.append([item, sold[item], money[item]])
    book.save(path)
    print(f"Saved {path}: {len(sold)} items")


if __name__ == "__main__":
    save_report(read_orders("orders.csv"), "report.xlsx")
