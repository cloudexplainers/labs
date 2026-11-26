# The SQL Roadmap for Beginners

Video: https://youtu.be/sjTBLMRD-cY  
Written version: https://cloudexplainers.com/the-sql-roadmap-for-beginners/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/make_seed.py`](lab/make_seed.py)
- [`lab/seed.sql`](lab/seed.sql)
- [`lab/start.sh`](lab/start.sh)
- [`lab/steps/add_member_v1.py`](lab/steps/add_member_v1.py)
- [`lab/steps/add_member_v2.py`](lab/steps/add_member_v2.py)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### Where you'll end up

```sh
club=> SELECT m.name, count(l.id) AS borrowed
  FROM members m
  LEFT JOIN loans l ON l.member_id = m.id
  GROUP BY m.name
  ORDER BY borrowed DESC;
```

### Stage 1: SELECT

```sh
club=> \dt
club=> SELECT title, author, year FROM books
  WHERE year < 1900
  ORDER BY year;
club=> SELECT title, year FROM books WHERE author = "Ursula K. Le Guin";
club=> SELECT title, year FROM books WHERE author = 'Ursula K. Le Guin';
```

### Stage 2: NULL

```sh
club=> SELECT book_id, member_id FROM loans
  WHERE returned_on = NULL;
club=> SELECT book_id, member_id, borrowed_on FROM loans
  WHERE returned_on IS NULL;
```

### Stage 3: counting

```sh
club=> SELECT member_id, count(*) AS loan_count FROM loans
  GROUP BY member_id
  ORDER BY loan_count DESC;
club=> SELECT member_id, borrowed_on, count(*) FROM loans
  GROUP BY member_id;
club=> SELECT member_id, count(*) AS loan_count FROM loans
  GROUP BY member_id
  HAVING count(*) >= 5
  ORDER BY loan_count DESC;
```

### Stage 4: joins

```sh
club=> SELECT m.name, count(*) AS borrowed
  FROM members m
  JOIN loans l ON l.member_id = m.id
  GROUP BY m.name
  ORDER BY borrowed DESC;
club=> SELECT m.name, count(*) AS borrowed
  FROM members m
  LEFT JOIN loans l ON l.member_id = m.id
  GROUP BY m.name
  ORDER BY borrowed DESC;
club=> SELECT m.name, b.title, l.borrowed_on
  FROM loans l
  JOIN members m ON m.id = l.member_id
  JOIN books b ON b.id = l.book_id
  WHERE l.returned_on IS NULL;
```

### Stage 5: designing tables

```sh
club=> CREATE TABLE reviews (
  id        integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  book_id   integer NOT NULL REFERENCES books (id),
  member_id integer NOT NULL REFERENCES members (id),
  stars     integer NOT NULL CHECK (stars BETWEEN 1 AND 5)
);
club=> INSERT INTO reviews (book_id, member_id, stars) VALUES (17, 1, 6);
club=> INSERT INTO reviews (book_id, member_id, stars) VALUES (99, 1, 5);
```

### Stage 6: changing data

```sh
club=> INSERT INTO loans (book_id, member_id, borrowed_on)
  VALUES (17, 2, current_date);
club=> UPDATE loans SET returned_on = current_date WHERE id = 23;
club=> BEGIN;
club=*> UPDATE loans SET returned_on = current_date;
club=*> SELECT count(*) FROM loans WHERE returned_on IS NULL;
club=*> ROLLBACK;
club=> SELECT count(*) FROM loans WHERE returned_on IS NULL;
```

### Stage 7: indexes

```sh
club=> CREATE TABLE practice_loans AS
  SELECT g AS id,
         (random() * 99999)::int + 1 AS member_id,
         date '2020-01-01' + (random() * 2000)::int AS borrowed_on
  FROM generate_series(1, 1000000) g;
club=> EXPLAIN (ANALYZE, COSTS OFF, TIMING OFF)
  SELECT * FROM practice_loans WHERE member_id = 4242;
club=> CREATE INDEX ON practice_loans (member_id);
club=> EXPLAIN (ANALYZE, COSTS OFF, TIMING OFF)
  SELECT * FROM practice_loans WHERE member_id = 4242;
```

### Stage 8: SQL in your code

```sh
# linda@laptop:~/club$
grep -n execute add_member.py
python3 add_member.py 'Rosa Diaz'
python3 add_member.py "Pat O'Brien"
python3 add_member.py "Pat O'Brien"
psql club -c "SELECT id, name FROM members WHERE id > 12;"
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
