-- Ana's tea shop: the tables every join in the video runs on.
CREATE TABLE customers (
  id          int PRIMARY KEY,
  name        text NOT NULL,
  referred_by int REFERENCES customers (id)   -- the customer who told them about the shop
);
CREATE TABLE orders (
  id          int PRIMARY KEY,
  customer_id int REFERENCES customers (id),   -- NULL = a guest checkout
  tea         text NOT NULL
);
CREATE TABLE teas  (tea  text PRIMARY KEY);
CREATE TABLE sizes (size text PRIMARY KEY);

INSERT INTO customers VALUES (1, 'Mia', NULL), (2, 'Leo', 1), (3, 'Sara', 1), (4, 'Ben', 2);
INSERT INTO orders VALUES (101, 1, 'Sencha'), (102, 1, 'Assam'), (103, 2, 'Earl Grey'),
                          (104, 3, 'Sencha'), (105, NULL, 'Oolong');
INSERT INTO teas  VALUES ('Sencha'), ('Assam'), ('Earl Grey'), ('Oolong');
INSERT INTO sizes VALUES ('small'), ('medium'), ('large');
