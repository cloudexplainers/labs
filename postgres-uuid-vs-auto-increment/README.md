# PostgreSQL UUID vs Auto Increment: Which Primary Key Should You Use?

Video: https://youtu.be/tewqLmPmyR4  
Written version: https://cloudexplainers.com/postgresql-uuid-vs-auto-increment-which-primary-key-should-you-use/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/init.sql`](lab/init.sql)
- [`lab/pgpass`](lab/pgpass)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### Two stores, both started at 1

```sh
# ana@laptop:~$
psql -h branch -c '\copy orders TO STDOUT' | psql -h store -c '\copy orders FROM STDIN'
psql -h store -c 'SELECT min(id), max(id), count(*) FROM orders'
psql -h branch -c 'SELECT min(id), max(id), count(*) FROM orders'
```

### What an auto increment key is

```sh
# ana@laptop:~$
psql -h store
records=> INSERT INTO orders (customer, album, total) VALUES ('Mia', 'Kind of Blue', 24.00) RETURNING id;
```

### What a counter gives away

```sh
records=> BEGIN;
records=> INSERT INTO orders (customer, album, total) VALUES ('Mia', 'Horses', 24.00) RETURNING id;
records=> ROLLBACK;
records=> INSERT INTO orders (customer, album, total) VALUES ('Mia', 'Horses', 24.00) RETURNING id;
records=> SELECT id, customer, album FROM orders WHERE id > 1042;
records=> SELECT id, ordered_at::date FROM orders WHERE customer = 'Leo';
```

### The counter that runs out

```sh
records=> CREATE TABLE gift_cards (id serial PRIMARY KEY, amount int);
records=> SELECT setval('gift_cards_id_seq', 2147483646);
records=> INSERT INTO gift_cards (amount) VALUES (25) RETURNING id;
records=> INSERT INTO gift_cards (amount) VALUES (25) RETURNING id;
```

### What a UUID is

```sh
records=> SELECT gen_random_uuid() FROM generate_series(1, 3);
records=> SELECT pg_column_size(1043::bigint) AS bigint, pg_column_size(uuidv7()) AS uuid;
# ana@laptop:~$
psql -h branch -c '\copy orders_uuid TO STDOUT' | psql -h store -c '\copy orders_uuid FROM STDIN'
psql -h store -c 'SELECT count(*) FROM orders_uuid'
```

### Random or time-ordered

```sh
records=> SELECT uuidv7() FROM generate_series(1, 3);
records=> SELECT id, uuid_extract_timestamp(id)::date FROM orders_uuid WHERE customer = 'Leo';
```

### Does the bigger key cost you?

```sh
records=> INSERT INTO bulk_bigint (customer, album, total) SELECT 'Mia', 'Blue', 24.00 FROM generate_series(1, 5000000);
records=> INSERT INTO bulk_v4 (customer, album, total) SELECT 'Mia', 'Blue', 24.00 FROM generate_series(1, 5000000);
records=> INSERT INTO bulk_v7 (customer, album, total) SELECT 'Mia', 'Blue', 24.00 FROM generate_series(1, 5000000);
# ana@laptop:~$
cat one_v4.sql
pgbench -h store -n -c 8 -T 15 -f one_bigint.sql 2>&1 | grep -E 'latency average|tps'
pgbench -h store -n -c 8 -T 15 -f one_v4.sql 2>&1 | grep -E 'latency average|tps'
pgbench -h store -n -c 8 -T 15 -f one_v7.sql 2>&1 | grep -E 'latency average|tps'
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
