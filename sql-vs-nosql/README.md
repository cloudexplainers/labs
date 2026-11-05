# SQL vs NoSQL: When Each One Wins

Video: https://youtu.be/JOpxlu35bVc  
Written version: https://cloudexplainers.com/sql-vs-nosql-when-each-one-wins/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/schema.sql`](lab/schema.sql)
- [`lab/seed.js`](lab/seed.js)

## Commands, in the order the video runs them

### One kettle, sold twice

```sh
shop=# UPDATE products SET stock = stock - 1 WHERE name = 'Copper kettle';
shop=# UPDATE products SET stock = stock - 1 WHERE name = 'Copper kettle';
shop> db.products.updateOne({name: "Copper kettle"}, {$inc: {stock: -1}})
shop> db.products.updateOne({name: "Copper kettle"}, {$inc: {stock: -1}})
shop> db.products.findOne({name: "Copper kettle"})
```

### The same order, two shapes

```sh
shop=# SELECT o.id, c.name AS customer, p.name AS product, i.qty FROM orders o JOIN customers c ON c.id = o.customer_id JOIN order_items i ON i.order_id = o.id JOIN products p ON p.id = i.product_id WHERE o.id = 1001;
shop> db.orders.findOne({_id: 1001})
```

### Where SQL wins

```sh
shop=# INSERT INTO orders (id, customer_id) VALUES (1004, 99);
shop> db.orders.insertOne({_id: 1004, customer_id: 99, items: []})
shop> db.customers.findOne({_id: 99})
shop=# BEGIN;
shop=*# UPDATE products SET stock = stock - 1 WHERE name = 'Glass kettle';
shop=*# INSERT INTO orders (id, customer_id) VALUES (1001, 2);
shop=!# ROLLBACK;
shop=# SELECT name, stock FROM products WHERE name = 'Glass kettle';
shop> db.products.updateOne({name: "Glass kettle"}, {$inc: {stock: -1}})
shop> db.orders.insertOne({_id: 1001, customer_id: 2, items: []})
shop> db.products.findOne({name: "Glass kettle"}, {_id: 0, name: 1, stock: 1})
shop=# SELECT c.name, sum(i.qty * i.price) AS spent FROM customers c JOIN orders o ON o.customer_id = c.id JOIN order_items i ON i.order_id = o.id GROUP BY c.name ORDER BY spent DESC;
```

### Where NoSQL wins

```sh
shop> db.products.insertOne({name: "Sencha green tea", price: 12.5, stock: 40, origin: "Japan", grams: 100})
shop=# INSERT INTO products (id, name, price, stock, origin, grams) VALUES (4, 'Sencha green tea', 12.50, 40, 'Japan', 100);
shop=# ALTER TABLE products ADD COLUMN origin text, ADD COLUMN grams int;
shop=# INSERT INTO products (id, name, price, stock, origin, grams) VALUES (4, 'Sencha green tea', 12.50, 40, 'Japan', 100);
shop=# SELECT name, origin, grams FROM products ORDER BY id;
```

### The lines are blurring

```sh
shop=# ALTER TABLE products ADD COLUMN details jsonb;
shop=# INSERT INTO products (id, name, price, stock, details) VALUES (5, 'Assam black tea', 9.00, 25, '{"origin": "India", "grams": 250, "caffeine": "high"}');
shop=# SELECT name, details->>'caffeine' AS caffeine FROM products WHERE details ? 'caffeine';
shop> db.runCommand({collMod: "products", validator: {stock: {$gte: 0}}})
shop> db.products.updateOne({name: "Copper kettle"}, {$inc: {stock: -1}})
shop> db.products.findOne({name: "Copper kettle"}, {_id: 0, name: 1, stock: 1})
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
