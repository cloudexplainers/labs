"""A tiny MCP server for the demo: the orders of a made-up coffee shop."""
from datetime import date
from mcp.server.mcpserver import MCPServer

TODAY = date(2026, 10, 24)  # fixed, so every run sees the same shop
ORDERS = [
    {"id": 1041, "customer": "Ana",   "item": "Espresso beans 1 kg", "promised": "2026-10-20", "status": "delivered"},
    {"id": 1042, "customer": "Ben",   "item": "Grinder",             "promised": "2026-10-19", "status": "in transit"},
    {"id": 1043, "customer": "Chloe", "item": "Decaf 500 g",         "promised": "2026-10-23", "status": "in transit"},
    {"id": 1044, "customer": "Dev",   "item": "Mugs (set of 4)",     "promised": "2026-10-27", "status": "packed"},
    {"id": 1045, "customer": "Eli",   "item": "Kettle",              "promised": "2026-10-22", "status": "delivered"},
]

mcp = MCPServer("orders")


def _days_late(o):
    if o["status"] == "delivered":
        return 0
    return max(0, (TODAY - date.fromisoformat(o["promised"])).days)


@mcp.tool()
def find_late_orders() -> list[dict]:
    """List orders that are past their promised delivery date and not delivered yet."""
    return [dict(o, days_late=_days_late(o)) for o in ORDERS if _days_late(o) > 0]


@mcp.tool()
def get_order(order_id: int) -> dict:
    """Get one order by its number."""
    for o in ORDERS:
        if o["id"] == order_id:
            return dict(o, days_late=_days_late(o))
    raise ValueError(f"No order {order_id}")


if __name__ == "__main__":
    mcp.run()
