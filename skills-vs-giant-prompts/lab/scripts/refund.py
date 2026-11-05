#!/usr/bin/env python3
"""Kettle & Bean refund calculator: the refund rules as code."""
import argparse

p = argparse.ArgumentParser()
p.add_argument("--price", type=float, required=True)
p.add_argument("--days", type=int, required=True, help="days since delivery")
p.add_argument("--opened", choices=["yes", "no"], required=True)
a = p.parse_args()

if a.opened == "no" and a.days <= 30:
    back, credit, rule = a.price, 0.0, "unopened, within 30 days: full refund"
elif a.days <= 14:
    back, credit, rule = a.price * 0.5, a.price, "opened, within 14 days: 50% back or 100% credit"
elif a.days <= 30:
    back, credit, rule = 0.0, a.price * 0.5, "opened, 15-30 days: 50% store credit"
else:
    back, credit, rule = 0.0, a.price * 0.25, "after 30 days: 25% store credit, once a year"

print(f"rule: {rule}")
print(f"refund to card: ${back:.2f}")
print(f"or store credit: ${credit:.2f}" if credit else "store credit: none")
