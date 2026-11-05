# How PostgreSQL Works

Video: https://youtu.be/llbqmoe-hNw  
Written version: https://cloudexplainers.com/how-postgresql-works/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/schema.sql`](lab/schema.sql)

## Commands, in the order the video runs them

### Saved, then a crash

```sh
shop=# INSERT INTO orders (customer_id, product_id, qty) VALUES (42, 1, 2) RETURNING id;
shop=# SELECT id, qty FROM orders WHERE id = 200001;
shop=# SELECT id, customer_id, qty, status FROM orders WHERE id = 200001;
```

### A process per connection

```sh
shop=# SELECT pg_backend_pid();
shop=# SELECT pg_backend_pid();
shop=# SELECT pid, backend_type FROM pg_stat_activity ORDER BY backend_type, pid;
```

### The planner

```sh
shop=# EXPLAIN SELECT * FROM orders WHERE customer_id = 42;
shop=# CREATE INDEX orders_customer_idx ON orders (customer_id);
shop=# EXPLAIN SELECT * FROM orders WHERE customer_id = 42;
shop=# SELECT count(*) FROM orders WHERE customer_id = 42;
```

### Shared buffers

```sh
shop=# SHOW shared_buffers;
shop=# SELECT buffers_evicted FROM pg_buffercache_evict_relation('orders');
shop=# EXPLAIN (ANALYZE, COSTS OFF, TIMING OFF) SELECT sum(qty) FROM orders;
shop=# EXPLAIN (ANALYZE, COSTS OFF, TIMING OFF) SELECT sum(qty) FROM orders;
```

### The write-ahead log

```sh
shop=# SELECT pg_current_wal_lsn();
shop=# INSERT INTO orders (customer_id, product_id, qty) VALUES (7, 3, 1);
shop=# SELECT pg_current_wal_lsn(), pg_wal_lsn_diff(pg_current_wal_lsn(), '0/3F96790') AS bytes;
shop=# INSERT INTO orders (customer_id, product_id, qty) VALUES (8, 4, 3);
shop=# SELECT pg_current_wal_lsn(), pg_wal_lsn_diff(pg_current_wal_lsn(), '0/3F99658') AS bytes;
```

### Row versions and VACUUM

```sh
shop=# BEGIN;
shop=*# UPDATE products SET price = 45.00 WHERE id = 1;
shop=*# SELECT ctid, xmin, xmax, name, price FROM products WHERE id = 1;
shop=# SELECT ctid, xmin, xmax, name, price FROM products WHERE id = 1;
shop=# UPDATE orders SET status = 'delivered' WHERE created_at < '2026-01-15';
shop=# SELECT n_dead_tup FROM pg_stat_user_tables WHERE relname = 'orders';
shop=# VACUUM orders;
shop=# SELECT n_dead_tup FROM pg_stat_user_tables WHERE relname = 'orders';
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
