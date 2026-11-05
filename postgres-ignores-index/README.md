# Why PostgreSQL Ignores Your Index

Video: https://youtu.be/wGEhRGsYbLg  
Written version: https://cloudexplainers.com/why-postgresql-ignores-your-index/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Commands, in the order the video runs them

### The symptom

```sh
EXPLAIN ANALYZE SELECT * FROM users WHERE lower(email) = 'user424242@example.com';
```

### Reading EXPLAIN ANALYZE

```sh
EXPLAIN SELECT * FROM users WHERE lower(email) = 'user424242@example.com';
```

### Reason 1: a function on the column

```sh
SELECT indexname, indexdef FROM pg_indexes WHERE tablename = 'users' ORDER BY indexname;
CREATE INDEX users_email_lower_idx ON users (lower(email));
ANALYZE users;
EXPLAIN ANALYZE SELECT * FROM users WHERE lower(email) = 'user424242@example.com';
```

### Reason 2: too many matching rows

```sh
SELECT plan, count(*) FROM users GROUP BY plan ORDER BY 2 DESC;
EXPLAIN SELECT * FROM users WHERE plan = 'free';
EXPLAIN SELECT * FROM users WHERE plan = 'enterprise';
```

### Reason 3: mismatched types

```sh
EXPLAIN SELECT * FROM users WHERE id = 42.0;
EXPLAIN SELECT * FROM users WHERE id = 42;
```

### Reason 4: a leading wildcard

```sh
EXPLAIN ANALYZE SELECT * FROM users WHERE email LIKE '%424242%';
CREATE EXTENSION pg_trgm;
CREATE INDEX users_email_trgm_idx ON users USING gin (email gin_trgm_ops);
EXPLAIN ANALYZE SELECT * FROM users WHERE email LIKE '%424242%';
```

### Reason 5: stale statistics

```sh
-- orders: 500,000 rows, all 'pending' when ANALYZE last ran
UPDATE orders SET status = 'shipped' WHERE id > 10;
EXPLAIN ANALYZE SELECT * FROM orders WHERE status = 'pending';
VACUUM ANALYZE orders;
EXPLAIN ANALYZE SELECT * FROM orders WHERE status = 'pending';
```

### Reason 6: tiny tables

```sh
EXPLAIN SELECT * FROM countries WHERE code = 'DE';
SELECT pg_size_pretty(pg_relation_size('countries')) AS table_size;
```

### Prevent it

```sh
SET auto_explain.log_min_duration = '50ms';  -- then any slow query
SELECT indexrelname AS index, idx_scan AS scans FROM pg_stat_user_indexes WHERE relname = 'users' ORDER BY idx_scan;
BEGIN;
=# EXPLAIN ANALYZE DELETE FROM users WHERE id < 10;
=# ROLLBACK;
=# SELECT count(*) FROM users WHERE id < 10;
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
