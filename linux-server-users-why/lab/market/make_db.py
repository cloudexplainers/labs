"""Fills the market's database: 40 products and 500,000 past orders from 20,000 customers."""
import random
import sqlite3

random.seed(145)
c = sqlite3.connect("/srv/market/market.db")
c.executescript("""
CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, stall TEXT, price REAL);
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, day TEXT, total REAL);
""")
items = ["Apples", "Pears", "Plums", "Carrots", "Kale", "Leeks", "Honey", "Eggs", "Sourdough", "Rye loaf",
         "Cheddar", "Goat cheese", "Jam", "Cider", "Tomatoes", "Potatoes", "Onions", "Garlic", "Basil", "Mint"]
stalls = ["Hill Farm", "Mill Bakery", "Brook Dairy", "Orchard Row"]
c.executemany("INSERT INTO products VALUES (?,?,?,?)",
              [(i + 1, f"{items[i % 20]}{'' if i < 20 else ' (large)'}", stalls[i % 4], round(1.5 + (i * 37 % 90) / 10, 2))
               for i in range(40)])
c.executemany("INSERT INTO orders VALUES (?,?,?,?)",
              [(i + 1, random.randint(1, 20000), f"2026-{random.randint(1, 10):02d}-{random.randint(1, 28):02d}",
                round(random.uniform(4, 60), 2)) for i in range(500000)])
c.commit()
