"""Shared helpers for the family recipe site."""
import html


def slug(name: str) -> str:
    return "-".join(name.lower().split())


def page(recipe: dict) -> str:
    items = "".join(f"<li>{html.escape(i)}</li>" for i in recipe["ingredients"])
    return f"<h1>{html.escape(recipe['name'])}</h1><p>From {html.escape(recipe['from'])}</p><ul>{items}</ul>\n"
