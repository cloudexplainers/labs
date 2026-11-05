import sqlite3

db = sqlite3.connect("shop.db")
for name, price in db.execute("SELECT name, price FROM teas"):
    print(f"{name:<10} ${price:.2f}")
