-- Ana's tea shop: 20 teas and a few million past orders.
CREATE TABLE products (
  id          int PRIMARY KEY,
  name        text NOT NULL,
  price_cents int  NOT NULL
);
CREATE TABLE orders (
  id         bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  product_id int NOT NULL,
  qty        int NOT NULL,
  ordered_at timestamptz NOT NULL
);
INSERT INTO products VALUES
 (1,'Sencha',1200),(2,'Assam',900),(3,'Earl Grey',1050),(4,'Jasmine Pearls',1800),(5,'Darjeeling',1400),
 (6,'Oolong',1300),(7,'Genmaicha',950),(8,'Rooibos',800),(9,'Chamomile',750),(10,'Peppermint',700),
 (11,'Matcha',2400),(12,'Hojicha',1100),(13,'Lapsang Souchong',1250),(14,'Ceylon',850),(15,'Gyokuro',2900),
 (16,'Pu-erh',2000),(17,'White Peony',1600),(18,'Chai',900),(19,'Lemon Verbena',850),(20,'Keemun',1150);
-- skewed on purpose, so some teas really are best sellers
INSERT INTO orders (product_id, qty, ordered_at)
SELECT 1 + floor(20 * power(random(), 2))::int, 1 + floor(random() * 3)::int,
       now() - random() * interval '3 years'
FROM generate_series(1, 4000000);
ANALYZE;
