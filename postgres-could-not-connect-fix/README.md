# How to Fix PostgreSQL 'Could Not Connect to Server'

Video: https://youtu.be/tion6mWXdOg  
Written version: https://cloudexplainers.com/how-to-fix-postgresql-could-not-connect-to-server/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/old/Dockerfile`](lab/old/Dockerfile)
- [`lab/rink/app.py`](lab/rink/app.py)
- [`lab/rink/rink.service`](lab/rink/rink.service)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### Where a connection can stop

```sh
# ana@rink-web:~$
psql -h rink-db -U rink rink
pg_isready -h rink-db
# ana@old-laptop:~$
psql -h rink-db -U rink rink
```

### Is PostgreSQL even running?

```sh
# ana@rink-db:~$
sudo -u postgres psql
sudo systemctl restart postgresql
systemctl status postgresql
pg_lsclusters
sudo systemctl start postgresql@16-main
sudo tail -n 5 /var/log/postgresql/postgresql-16-main.log
grep -n '^shared_buffers' /etc/postgresql/16/main/postgresql.conf
sudo systemctl start postgresql@16-main
pg_lsclusters
```

### Running again

```sh
# ana@rink-web:~$
psql -h rink-db -U rink rink
# ana@rink-db:~$
sudo ss -ltn 'sport = :5432'
sudo -u postgres psql -c 'SHOW listen_addresses'
echo "listen_addresses = '*'" | sudo tee /etc/postgresql/16/main/conf.d/listen.conf
sudo systemctl reload postgresql@16-main
# ana@rink-web:~$
psql -h rink-db -U rink rink
# ana@rink-db:~$
sudo tail -n 3 /var/log/postgresql/postgresql-16-main.log
sudo systemctl restart postgresql@16-main
sudo ss -ltn 'sport = :5432'
```

### A new error means progress

```sh
# ana@rink-web:~$
psql -h rink-db -U rink rink
# ana@rink-db:~$
echo 'host  rink  rink  192.168.71.20/32  scram-sha-256' | sudo tee -a /etc/postgresql/16/main/pg_hba.conf
sudo systemctl reload postgresql@16-main
# ana@rink-web:~$
psql -h rink-db -U rink rink -c 'SELECT * FROM sessions'
psql -h rink-db -p 5433 -U rink rink
```

### When it hangs instead

```sh
# ana@rink-web:~$
ping -c 2 -n rink-db
PGCONNECT_TIMEOUT=10 psql -h rink-db -U rink rink
# ana@rink-db:~$
sudo ufw status
sudo ufw allow from 192.168.71.0/24 to any port 5432
# ana@rink-web:~$
psql -h rink-db -U rink rink -c 'SELECT count(*) FROM sessions'
```

### Before you call it fixed

```sh
# ana@rink-web:~$
pg_isready -h rink-db
# ana@rink-db:~$
pg_lsclusters
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
