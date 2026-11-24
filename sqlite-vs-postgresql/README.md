# SQL Databases: SQLite vs PostgreSQL

Video: https://youtu.be/HP8IEjLjQ1g  
Written version: https://cloudexplainers.com/sql-databases-sqlite-vs-postgresql/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/make_listings.py`](lab/make_listings.py)
- [`lab/pgpass`](lab/pgpass)
- [`lab/site/add_listing.py`](lab/site/add_listing.py)
- [`lab/site/lookups.py`](lab/site/lookups.py)
- [`lab/start.sh`](lab/start.sh)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### Same insert, two answers

```sh
# joe@office:~/site$
sqlite3 listings.db "INSERT INTO listings (address, price) VALUES ('12 Elm St', 'call us');"
psql listings -c "INSERT INTO listings (address, price) VALUES ('12 Elm St', 'call us');"
```

### A file, or a server

```sh
# joe@office:~/site$
ls -l
head -c 16 listings.db; echo
ps -e -o user,cmd | grep -E '^(postgres|USER)' | head -8
ss -ltn
```

### What each one lets in

```sh
# joe@office:~/site$
sqlite3 listings.db "SELECT address, price, typeof(price) FROM listings WHERE address = '12 Elm St';"
sqlite3 -table listings.db "SELECT address, price FROM listings ORDER BY price DESC LIMIT 3;"
sqlite3 listings.db "CREATE TABLE listings_strict (id INTEGER PRIMARY KEY, address TEXT, price INTEGER) STRICT; INSERT INTO listings_strict (address, price) VALUES ('12 Elm St', 'call us');"
```

### Reaching it from another PC

```sh
# jess@jess-pc:~$
psql -h office -d listings -c "SELECT count(*) FROM listings;"
psql -h office -d listings -c "INSERT INTO listings (address, price, beds) VALUES ('9 Lake Rd', 415000, 3);"
```

### Two writers at the same moment

```sh
# joe@office:~/site$
sqlite3 listings.db
sqlite> BEGIN IMMEDIATE;
sqlite> UPDATE listings SET price = price - 5000 WHERE id = 1;
# joe@office:~/site$
time python3 add_listing.py sqlite '4 Oak Ave' 389000
psql listings
listings=> BEGIN;
listings=> UPDATE listings SET price = price - 5000 WHERE id = 1;
# joe@office:~/site$
time python3 add_listing.py postgres '4 Oak Ave' 389000
```

### Which one is faster?

```sh
# joe@office:~/site$
python3 lookups.py
```

### Who may do what

```sh
# jess@jess-pc:~$
psql -h office -d listings -c "DELETE FROM listings;"
```

### Backing it up

```sh
# joe@office:~/site$
sqlite3 listings.db '.backup listings-copy.db'
pg_dump listings > listings.sql
ls -l listings-copy.db listings.sql
grep -m 3 -E '^(CREATE TABLE|COPY|GRANT)' listings.sql
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
