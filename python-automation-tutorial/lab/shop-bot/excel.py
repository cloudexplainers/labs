from pathlib import Path

from openpyxl import load_workbook
from openpyxl.styles import Font

path = Path.home() / "shop" / "report.xlsx"


def run():
    book = load_workbook(path)
    sheet = book["By tea"]
    sheet.column_dimensions["A"].width = 18
    for cell in sheet["C"][1:]:
        cell.number_format = "$#,##0.00"

    last = sheet.max_row
    sheet.cell(last + 1, 1, "Total").font = Font(bold=True)
    sheet.cell(last + 1, 3, f"=SUM(C2:C{last})").font = Font(bold=True)
    book.save(path)

    for row in sheet.iter_rows(values_only=True):
        print(row)


if __name__ == "__main__":
    run()
