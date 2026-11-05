# Why SQLite Is the Most Used Database in the World

Video: https://youtu.be/vXHFstokrRY  
Written version: https://cloudexplainers.com/why-sqlite-is-the-most-used-database-in-the-world/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/shop/lookups.py`](lab/shop/lookups.py)
- [`lab/shop/menu.py`](lab/shop/menu.py)
- [`lab/shop/restock.py`](lab/shop/restock.py)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### Reason 1: there's no server

```sh
# ana@laptop:~/shop$
sqlite3 shop.db "CREATE TABLE teas (name TEXT, price REAL, stock INTEGER);"
sqlite3 shop.db "INSERT INTO teas VALUES ('Sencha', 6.5, 40), ('Earl Grey', 5.0, 25), ('Oolong', 7.0, 12);"
sqlite3 -table shop.db "SELECT * FROM teas;"
ps -e
dpkg -l | grep -ci -e mysql -e postgres -e mariadb
ls -l shop.db
```

### Reason 2: the database is one file

```sh
# ana@laptop:~/shop$
file shop.db
head -c 15 shop.db; echo
cat menu.py
python3 menu.py
```

### Reason 3: small and fast

```sh
# ana@laptop:~/shop$
ls -lh orders.db
python3 lookups.py
```

### Reason 4: a crash can't half-save

```sh
# ana@laptop:~/shop$
sqlite3 -table shop.db "SELECT name, stock FROM teas;"
python3 restock.py
pkill -9 -f restock.py
ls -l shop.db*
python3 restock.py
sqlite3 -table shop.db "SELECT name, stock FROM teas;"
sqlite3 shop.db "PRAGMA integrity_check;"
python3 restock.py
sqlite3 -table shop.db "SELECT name, stock FROM teas;"
```

### The one job it's wrong for

```sh
# ana@laptop:~/shop$
sqlite3 shop.db
sqlite> BEGIN IMMEDIATE;
sqlite> UPDATE teas SET price = 7.5 WHERE name = 'Sencha';
# ana@laptop:~/shop$
sqlite3 shop.db "INSERT INTO teas VALUES ('Rooibos', 4.5, 30);"
sqlite3 shop.db "SELECT count(*) FROM teas;"
sqlite3 -cmd ".timeout 5000" shop.db "INSERT INTO teas VALUES ('Rooibos', 4.5, 30);"
sqlite> COMMIT;
# ana@laptop:~/shop$
sqlite3 shop.db "SELECT count(*) FROM teas;"
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
