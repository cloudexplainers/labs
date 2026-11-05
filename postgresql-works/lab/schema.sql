-- Ana's tea shop: the database for P066 "How PostgreSQL Works" (loaded off-screen by demo.sh).
CREATE EXTENSION pg_buffercache;
CREATE EXTENSION pageinspect;
CREATE TABLE customers (id int PRIMARY KEY, name text NOT NULL);
CREATE TABLE products (id int PRIMARY KEY, name text NOT NULL, price numeric(8,2) NOT NULL, stock int NOT NULL);
CREATE TABLE orders (
  id bigserial PRIMARY KEY,
  customer_id int NOT NULL REFERENCES customers,
  product_id int NOT NULL,
  qty int NOT NULL,
  status text NOT NULL DEFAULT 'new',
  created_at timestamptz NOT NULL DEFAULT now()
);
INSERT INTO customers SELECT g, 'Customer ' || g FROM generate_series(1, 5000) g;
INSERT INTO products VALUES (1, 'Copper kettle', 49.00, 12), (2, 'Glass teapot', 32.00, 20),
  (3, 'Sencha green tea', 12.50, 40), (4, 'Assam black tea', 9.00, 25);
SELECT setseed(0.66);
INSERT INTO orders (customer_id, product_id, qty, status, created_at)
SELECT 1 + floor(random() * 5000)::int, 1 + floor(random() * 4)::int, 1 + floor(random() * 3)::int, 'shipped',
       timestamptz '2026-01-01' + g * interval '1 minute'
FROM generate_series(1, 200000) g;
