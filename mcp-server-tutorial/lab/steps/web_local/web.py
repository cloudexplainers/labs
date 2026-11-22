import csv
from pathlib import Path

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ResourceNotFoundError, ToolError

mcp = MCPServer("car-lot")
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


@mcp.tool()
def mark_sold(stock: str) -> str:
    """Mark one car as sold, by its stock number (like A12)."""
    cars = load()
    for c in cars:
        if c["stock"] == stock:
            c["status"] = "sold"
            with open(CARS, "w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=cars[0].keys())
                w.writeheader()
                w.writerows(cars)
            return f"{stock} is marked sold"
    raise ToolError(f"No car with stock number {stock}")


@mcp.resource("lot://cars/{stock}")
def car(stock: str) -> dict:
    """One car's full record, by its stock number."""
    for c in load():
        if c["stock"] == stock:
            return c
    raise ResourceNotFoundError(f"No car with stock number {stock}")


@mcp.prompt()
def write_listing(stock: str) -> str:
    """Write a short, honest ad for one car."""
    return (f"Read lot://cars/{stock} and write a three-sentence ad for it. "
            "Mention the year, the miles and the price. No hype.")


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
