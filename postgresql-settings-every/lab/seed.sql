-- The bake sale's orders: 600,000 rows of made-up orders (families, items, totals), the size a busy school's
-- online orders reach over a few years. Run off-screen once, as the bakesale role.
CREATE TABLE orders (
  id      bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  family  text    NOT NULL,
  item    text    NOT NULL,
  total   numeric(8,2) NOT NULL,
  status  text    NOT NULL DEFAULT 'new',
  note    text    NOT NULL DEFAULT ''
);
INSERT INTO orders (family, item, total, status, note)
SELECT 'family-' || (g % 4000),
       (ARRAY['brownies','cupcakes','lemon bars','cookies','banana bread','pie'])[1 + g % 6],
       round((2 + (g::bigint * 7919 % 4000) / 100.0)::numeric, 2),
       (ARRAY['new','paid','picked up'])[1 + g % 3],
       'order ' || g || CASE WHEN g % 97 = 0 THEN ' nut free please' ELSE '' END
FROM generate_series(1, 600000) g;
ANALYZE orders;
