import csv
from pathlib import Path

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("car-lot")
CARS = Path(__file__).parent / "cars.csv"


def load():
    with open(CARS) as f:
        return list(csv.DictReader(f))


@mcp.tool()
def search_cars(body: str, color: str, max_price: int) -> list[dict]:
    """Find cars for sale by body style (hatchback, sedan, suv, wagon),
    colour, and the most the customer will pay, in dollars."""
    return [c for c in load()
            if c["status"] == "for sale" and c["body"] == body
            and c["color"] == color and int(c["price"]) <= max_price]


if __name__ == "__main__":
    mcp.run()
