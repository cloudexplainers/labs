# Every PostgreSQL Setting to Change After You Install It

Video: https://youtu.be/WUPZQ9pPoo0  
Written version: https://cloudexplainers.com/every-postgresql-setting-to-change-after-you-install-it/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/seed.sql`](lab/seed.sql)

## Commands, in the order the video runs them

### How a setting changes

```sh
# chris@bakesale-db:~$
sudo -u postgres psql -c "SELECT name, setting, unit, context FROM pg_settings WHERE name IN ('listen_addresses','shared_buffers','effective_cache_size','work_mem','maintenance_work_mem','log_min_duration_statement','idle_in_transaction_session_timeout') ORDER BY name;"
free -h
```

### listen_addresses

```sh
# chris@orders:~$
psql -h bakesale-db -U bakesale bakesale -c "SELECT 1;"
# chris@bakesale-db:~$
sudo -u postgres psql -c "SHOW listen_addresses;"
sudo -u postgres psql -c "ALTER SYSTEM SET listen_addresses = '*';"
sudo -u postgres psql -c "SELECT name, setting, pending_restart FROM pg_settings WHERE name = 'listen_addresses';"
sudo systemctl restart postgresql
sudo -u postgres psql -c "SHOW listen_addresses;"
```

### pg_hba.conf

```sh
# chris@orders:~$
psql -h bakesale-db -U bakesale bakesale -c "SELECT 1;"
sudo grep -Ev '^#|^$' /etc/postgresql/16/main/pg_hba.conf
# chris@bakesale-db:~$
echo 'host  bakesale  bakesale  10.236.135.211/32  scram-sha-256' | sudo tee -a /etc/postgresql/16/main/pg_hba.conf
sudo -u postgres psql -c "SELECT pg_reload_conf();"
# chris@orders:~$
psql -h bakesale-db -U bakesale bakesale -c "SELECT count(*) FROM orders;"
```

### shared_buffers

```sh
# chris@bakesale-db:~$
sudo -u postgres psql -c "SHOW shared_buffers;"
sudo -u postgres psql -c "ALTER SYSTEM SET shared_buffers = '1GB';" -c "ALTER SYSTEM SET effective_cache_size = '3GB';"
sudo systemctl restart postgresql
sudo -u postgres psql -c "SHOW shared_buffers;" -c "SHOW effective_cache_size;"
```

### work_mem

```sh
sudo -u postgres psql bakesale -c "EXPLAIN (ANALYZE, COSTS OFF, TIMING OFF) SELECT family, item, total FROM orders ORDER BY family, total DESC;"
sudo -u postgres psql bakesale -c "SET work_mem = '128MB';" -c "EXPLAIN (ANALYZE, COSTS OFF, TIMING OFF) SELECT family, item, total FROM orders ORDER BY family, total DESC;"
# chris@bakesale-db:~$
sudo -u postgres psql -c "ALTER SYSTEM SET work_mem = '16MB';" -c "SELECT pg_reload_conf();"
```

### maintenance_work_mem

```sh
# chris@bakesale-db:~$
sudo -u postgres psql bakesale -c '\timing on' -c 'CREATE INDEX orders_family_idx ON orders (family, item, total);'
sudo -u postgres psql -c "ALTER SYSTEM SET maintenance_work_mem = '256MB';" -c "SELECT pg_reload_conf();"
sudo -u postgres psql bakesale -c '\timing on' -c 'CREATE INDEX orders_family_idx ON orders (family, item, total);'
```

### log_min_duration_statement

```sh
# chris@bakesale-db:~$
sudo -u postgres psql -c "ALTER SYSTEM SET log_min_duration_statement = '250ms';" -c "SELECT pg_reload_conf();"
# chris@orders:~$
psql -h bakesale-db -U bakesale bakesale -c "\timing on" -c "SELECT count(DISTINCT (family, note)) FROM orders;"
# chris@bakesale-db:~$
sudo tail -n 1 /var/log/postgresql/postgresql-16-main.log
```

### idle_in_transaction_session_timeout

```sh
# sarah@orders:~$
psql -h bakesale-db -U bakesale bakesale
bakesale=> BEGIN;
bakesale=*> UPDATE orders SET status = 'paid' WHERE id = 42;
# chris@orders:~$
psql -h bakesale-db -U bakesale bakesale -c "UPDATE orders SET status = 'picked up' WHERE id = 42;"
# chris@bakesale-db:~$
sudo -u postgres psql -P pager=off -c "SELECT pid, usename, state, now() - state_change AS for, left(query, 48) AS query FROM pg_stat_activity WHERE datname = 'bakesale' ORDER BY state;"
^C
# chris@bakesale-db:~$
sudo -u postgres psql -c "ALTER SYSTEM SET idle_in_transaction_session_timeout = '10s';" -c "SELECT pg_reload_conf();"
# chris@orders:~$
psql -h bakesale-db -U bakesale bakesale -c "UPDATE orders SET status = 'picked up' WHERE id = 42;"
bakesale=*> SELECT status FROM orders WHERE id = 42;
```

### Recap

```sh
# chris@bakesale-db:~$
sudo -u postgres cat /var/lib/postgresql/16/main/postgresql.auto.conf
# chris@orders:~$
psql -h bakesale-db -U bakesale bakesale -c "SELECT status, count(*) FROM orders GROUP BY status ORDER BY status;"
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
