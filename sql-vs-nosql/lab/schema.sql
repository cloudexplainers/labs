-- Ana's kettle shop in PostgreSQL (P009). Loaded off-screen by demo.sh.
CREATE TABLE customers (
  id    int PRIMARY KEY,
  name  text NOT NULL,
  email text NOT NULL UNIQUE
);
CREATE TABLE products (
  id    int PRIMARY KEY,
  name  text NOT NULL UNIQUE,
  price numeric(8,2) NOT NULL,
  stock int NOT NULL CHECK (stock >= 0)
);
CREATE TABLE orders (
  id          int PRIMARY KEY,
  customer_id int NOT NULL REFERENCES customers(id),
  placed      date NOT NULL DEFAULT current_date
);
CREATE TABLE order_items (
  order_id   int NOT NULL REFERENCES orders(id),
  product_id int NOT NULL REFERENCES products(id),
  qty        int NOT NULL CHECK (qty > 0),
  price      numeric(8,2) NOT NULL,
  PRIMARY KEY (order_id, product_id)
);
INSERT INTO customers VALUES
  (1, 'Ben', 'ben@example.com'),
  (2, 'Cara', 'cara@example.com'),
  (3, 'Dev', 'dev@example.com');
INSERT INTO products VALUES
  (1, 'Copper kettle', 89.00, 1),
  (2, 'Glass kettle', 54.00, 12),
  (3, 'Travel kettle', 32.50, 30);
INSERT INTO orders (id, customer_id) VALUES (1001, 1), (1002, 2), (1003, 1);
INSERT INTO order_items VALUES
  (1001, 2, 1, 54.00), (1001, 3, 2, 32.50),
  (1002, 3, 1, 32.50),
  (1003, 2, 1, 54.00);
