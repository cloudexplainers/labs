# PostgreSQL: Full Tutorial for Beginners

Video: https://youtu.be/B93DpU3vWNY  
Written version: https://cloudexplainers.com/postgresql-full-tutorial-for-beginners/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### A campground's bookings

```sh
campground=> INSERT INTO bookings (site_id, guest_id, arrive, leave)
  VALUES (5, 4, '2027-07-31', '2027-08-02');
```

### Installing it

```sh
# ana@office:~$
psql --version
sudo apt install -y postgresql
pg_lsclusters
psql --version
psql
sudo -u postgres psql
postgres=# SELECT current_user;
postgres=# CREATE USER ana CREATEDB;
# ana@office:~$
createdb campground
psql campground
campground=> \conninfo
campground=> \dt
```

### Your first table

```sh
campground=> CREATE TABLE sites (
  id     integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name   text NOT NULL UNIQUE,
  kind   text NOT NULL,
  people integer NOT NULL CHECK (people > 0),
  price  numeric(6,2) NOT NULL CHECK (price > 0)
);
campground=> SELECT 0.1::float8 + 0.2::float8 AS float, 0.1::numeric + 0.2::numeric AS numeric;
campground=> \d sites
campground=> INSERT INTO sites (name, kind, people, price) VALUES ("Lakeside 1", "tent", 4, 32);
campground=> INSERT INTO sites (name, kind, people, price) VALUES
  ('Lakeside 1', 'tent', 4, 32),
  ('Lakeside 2', 'tent', 4, 32),
  ('Lakeside 3', 'tent', 6, 36),
  ('Meadow 4', 'tent', 6, 28),
  ('Meadow 5', 'tent', 8, 30),
  ('Pine Cabin 6', 'cabin', 4, 85),
  ('Pine Cabin 7', 'cabin', 6, 95),
  ('Creek RV 8', 'rv', 4, 45);
```

### Asking with SELECT

```sh
campground=> SELECT * FROM sites;
campground=> SELECT name, people, price FROM sites
  WHERE kind = 'tent' AND people >= 6
  ORDER BY price;
campground=> SELECT kind, count(*), min(price) FROM sites GROUP BY kind ORDER BY kind;
```

### Rules the data must follow

```sh
campground=> INSERT INTO sites (name, kind, people, price) VALUES ('Lakeside 9', 'tent', 0, 32);
campground=> INSERT INTO sites (name, kind, people, price) VALUES ('Lakeside 9', 'tent', 'four', 32);
campground=> INSERT INTO sites (name, kind, people, price) VALUES ('Lakeside 1', 'tent', 4, 32);
campground=> INSERT INTO sites (name, kind, people) VALUES ('Lakeside 9', 'tent', 4);
```

### Changing and deleting rows

```sh
campground=> UPDATE sites SET price = 34 WHERE name = 'Lakeside 1';
campground=> BEGIN;
campground=*> UPDATE sites SET price = 99;
campground=*> SELECT name, price FROM sites ORDER BY id;
campground=*> ROLLBACK;
campground=> SELECT name, price FROM sites ORDER BY id;
campground=> DELETE FROM sites WHERE name = 'Creek RV 8';
```

### Tables that point at each other

```sh
campground=> CREATE TABLE guests (
  id    integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name  text NOT NULL,
  email text NOT NULL UNIQUE,
  phone text
);
campground=> INSERT INTO guests (name, email, phone) VALUES
  ('Mia Chen', 'mia@example.com', '555-0101'),
  ('Leo Park', 'leo@example.com', '555-0102'),
  ('Sara Diaz', 'sara@example.com', '555-0103'),
  ('Tom Reed', 'tom@example.com', '555-0104'),
  ('Ava Brooks', 'ava@example.com', NULL);
campground=> SELECT name FROM guests WHERE phone = NULL;
campground=> SELECT name FROM guests WHERE phone IS NULL;
campground=> CREATE TABLE bookings (
  id       integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  site_id  integer NOT NULL REFERENCES sites,
  guest_id integer NOT NULL REFERENCES guests,
  arrive   date NOT NULL,
  leave    date NOT NULL CHECK (leave > arrive)
);
campground=> INSERT INTO bookings (site_id, guest_id, arrive, leave) VALUES
  (1, 1, '2027-07-09', '2027-07-11'),
  (6, 2, '2027-07-09', '2027-07-12'),
  (3, 3, '2027-07-02', '2027-07-05'),
  (4, 4, '2027-07-09', '2027-07-11'),
  (1, 3, '2027-07-16', '2027-07-18'),
  (7, 1, '2027-08-06', '2027-08-08');
campground=> \dt
campground=> INSERT INTO bookings (site_id, guest_id, arrive, leave)
  VALUES (8, 5, '2027-07-23', '2027-07-25');
campground=> DELETE FROM guests WHERE name = 'Leo Park';
campground=> INSERT INTO bookings (site_id, guest_id, arrive, leave)
  VALUES (5, 5, '2027-07-25', '2027-07-23');
```

### Joining tables

```sh
campground=> SELECT g.name AS guest, s.name AS site, b.arrive, b.leave
FROM bookings b
JOIN guests g ON g.id = b.guest_id
JOIN sites s ON s.id = b.site_id
ORDER BY b.arrive;
campground=> SELECT g.name, count(*) AS stays
FROM bookings b JOIN guests g ON g.id = b.guest_id
GROUP BY g.name
HAVING count(*) > 1;
campground=> SELECT s.name, count(b.id) AS bookings
FROM sites s
JOIN bookings b ON b.site_id = s.id
GROUP BY s.name
ORDER BY s.name;
campground=> SELECT s.name, count(b.id) AS bookings
FROM sites s
LEFT JOIN bookings b ON b.site_id = s.id
GROUP BY s.name
ORDER BY s.name;
campground=> SELECT s.name, sum((b.leave - b.arrive) * s.price) AS revenue
FROM bookings b JOIN sites s ON s.id = b.site_id
GROUP BY s.name ORDER BY revenue DESC;
campground=> SELECT name, price FROM sites s
WHERE NOT EXISTS (
  SELECT 1 FROM bookings b
  WHERE b.site_id = s.id
    AND b.arrive < '2027-07-11' AND b.leave > '2027-07-09')
ORDER BY name;
```

### Making it fast with an index

```sh
campground=> \timing on
campground=> CREATE TABLE guest_test (LIKE guests INCLUDING ALL);
campground=> INSERT INTO guest_test (name, email, phone)
SELECT 'Guest ' || n, 'guest' || n || '@example.com', '555-' || lpad(n::text, 7, '0')
FROM generate_series(1, 1000000) AS n;
campground=> EXPLAIN (ANALYZE, COSTS OFF, TIMING OFF)
  SELECT * FROM guest_test WHERE phone = '555-0765432';
campground=> CREATE INDEX ON guest_test (phone);
campground=> EXPLAIN (ANALYZE, COSTS OFF, TIMING OFF)
  SELECT * FROM guest_test WHERE phone = '555-0765432';
campground=> SELECT pg_size_pretty(pg_relation_size('guest_test')) AS table_size,
       pg_size_pretty(pg_relation_size('guest_test_phone_idx')) AS index_size;
campground=> \di guest_test*
campground=> DROP TABLE guest_test;
```

### Users and permissions

```sh
campground=> CREATE USER ben;
# ana@office:~$
sudo -u postgres createuser ben
campground=> GRANT SELECT ON sites, guests, bookings TO ben;
campground=> GRANT INSERT ON bookings TO ben;
campground=> SELECT name, price FROM sites ORDER BY id LIMIT 3;
campground=> DELETE FROM bookings WHERE id = 2;
campground=> UPDATE sites SET price = 1;
```

### Two bookings at once

```sh
campground=> BEGIN;
campground=*> SELECT count(*) FROM bookings
  WHERE site_id = 7 AND arrive < '2027-07-25' AND leave > '2027-07-23';
campground=*> SELECT count(*) FROM bookings
  WHERE site_id = 7 AND arrive < '2027-07-25' AND leave > '2027-07-23';
campground=*> INSERT INTO bookings (site_id, guest_id, arrive, leave)
  VALUES (7, 4, '2027-07-23', '2027-07-25');
campground=*> COMMIT;
campground=> SELECT b.id, g.name, b.arrive, b.leave FROM bookings b
  JOIN guests g ON g.id = b.guest_id WHERE b.site_id = 7 ORDER BY b.id;
campground=> CREATE EXTENSION btree_gist;
campground=> ALTER TABLE bookings ADD CONSTRAINT no_double_booking
  EXCLUDE USING gist (site_id WITH =, daterange(arrive, leave) WITH &&);
campground=> DELETE FROM bookings WHERE id = 10;
campground=> ALTER TABLE bookings ADD CONSTRAINT no_double_booking
  EXCLUDE USING gist (site_id WITH =, daterange(arrive, leave) WITH &&);
campground=> BEGIN;
campground=*> INSERT INTO bookings (site_id, guest_id, arrive, leave)
  VALUES (5, 2, '2027-07-30', '2027-08-01');
campground=> SELECT count(*) FROM bookings WHERE site_id = 5;
campground=> INSERT INTO bookings (site_id, guest_id, arrive, leave)
  VALUES (5, 4, '2027-07-31', '2027-08-02');
campground=*> COMMIT;
campground=> SELECT count(*) FROM bookings WHERE site_id = 5;
```

### From a program

```sh
# ben@office:~$
cat free_sites.py
python3 free_sites.py 2027-07-23 2027-07-25
python3 free_sites.py "2027-07-23'; DROP TABLE bookings; --" 2027-07-25
psql campground -c 'SELECT count(*) FROM bookings;'
```

### Backups

```sh
# ana@office:~$
pg_dump campground > campground.sql
ls -lh campground.sql
grep -E '^(CREATE TABLE|COPY|ALTER TABLE ONLY public.bookings)' campground.sql
psql campground -c 'DROP TABLE bookings;'
psql campground -c 'SELECT count(*) FROM bookings;'
dropdb campground
createdb campground
psql -q -o /dev/null -f campground.sql campground
psql campground -c 'SELECT count(*) FROM bookings;'
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
