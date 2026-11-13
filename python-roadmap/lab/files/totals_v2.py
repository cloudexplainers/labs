import csv


def read_orders(path):
    with open(path) as f:
        return list(csv.DictReader(f))


def totals(orders):
    sold = {}
    for row in orders:
        item = row["item"]
        sold[item] = sold.get(item, 0) + int(row["qty"])
    return sold


for item, qty in totals(read_orders("orders.csv")).items():
    print(f"{item}: {qty}")
