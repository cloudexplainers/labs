from pathlib import Path

import pandas as pd

shop = Path.home() / "shop"


def run():
    files = sorted((shop / "orders").glob("*/*.csv"))
    orders = pd.concat(pd.read_csv(f) for f in files)
    print(f"{len(orders)} orders in {len(files)} files")

    by_tea = orders.groupby("tea").agg(packs=("qty", "sum"),
                                       sales=("price", "sum"))
    by_tea = by_tea.sort_values("sales", ascending=False)
    print(by_tea)

    by_tea.to_excel(shop / "report.xlsx", sheet_name="By tea")
    print("Saved report.xlsx")


if __name__ == "__main__":
    run()
