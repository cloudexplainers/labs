# How to Fix PostgreSQL 'Password Authentication Failed'

Video: https://youtu.be/j_Xz07jw9yU  
Written version: https://cloudexplainers.com/how-to-fix-postgresql-password-authentication-failed/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/office/Dockerfile`](lab/office/Dockerfile)
- [`lab/office/school/book.py`](lab/office/school/book.py)
- [`lab/office/school/booking.env`](lab/office/school/booking.env)
- [`lab/office/testdb/compose.yaml`](lab/office/testdb/compose.yaml)
- [`lab/server/Dockerfile`](lab/server/Dockerfile)

## Commands, in the order the video runs them

### Refused, and it won't say why

```sh
# ana@office:~/school$
python3 book.py
psql -h lessons -U booking school
```

### The reason is in the server's log

```sh
# ana@lessons:~$
sudo tail -n 2 /var/log/postgresql/postgresql-16-main.log
sudo -u postgres psql -c '\password booking'
# ana@office:~/school$
python3 book.py
```

### Wrong user, same message

```sh
# ana@office:~/school$
python3 book.py
# ana@lessons:~$
sudo tail -n 3 /var/log/postgresql/postgresql-16-main.log
```

### On the server itself: peer

```sh
# ana@lessons:~$
psql -U booking school
sudo grep -v '^#' /etc/postgresql/16/main/pg_hba.conf | grep .
psql -h localhost -U booking school -c 'SELECT count(*) FROM lessons'
```

### A user with no password

```sh
# ana@lessons:~$
sudo -u postgres createuser ben
# ana@office:~/school$
psql -h lessons -U ben school
# ana@lessons:~$
sudo tail -n 3 /var/log/postgresql/postgresql-16-main.log
sudo -u postgres psql -c '\password ben'
# ana@office:~/school$
psql -h lessons -U ben school -c 'SELECT current_user'
```

### The right password, still refused

```sh
# ana@office:~/school$
psql -h lessons -U piano school
# ana@lessons:~$
sudo tail -n 3 /var/log/postgresql/postgresql-16-main.log
sudo -u postgres psql -c "SELECT rolname, left(rolpassword, 14) AS stored FROM pg_authid WHERE rolname IN ('booking', 'piano')"
sudo -u postgres psql -c '\password piano'
sudo -u postgres psql -c "SELECT rolname, left(rolpassword, 14) AS stored FROM pg_authid WHERE rolname IN ('booking', 'piano')"
# ana@office:~/school$
psql -h lessons -U piano school -c 'SELECT current_user'
```

### PostgreSQL in Docker

```sh
# ana@office:~/testdb$
grep PASSWORD compose.yaml
docker compose up -d
psql -h localhost -U postgres
docker compose logs db | grep -i skipping
docker compose exec db psql -U postgres -c '\password'
psql -h localhost -U postgres -c 'SELECT current_user'
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
