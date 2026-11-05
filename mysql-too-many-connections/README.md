# How to Fix MySQL Too Many Connections Database Errors

Video: https://youtu.be/BcVGcGekReQ  
Written version: https://cloudexplainers.com/how-to-fix-mysql-too-many-connections-database-errors/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/schema.sql`](lab/schema.sql)
- [`lab/shop/db.py`](lab/shop/db.py)
- [`lab/shop/hold.py`](lab/shop/hold.py)
- [`lab/shop/orders.py`](lab/shop/orders.py)
- [`lab/shop/orders_pool.py`](lab/shop/orders_pool.py)
- [`lab/shop/payment.py`](lab/shop/payment.py)
- [`lab/shop/rush.py`](lab/shop/rush.py)
- [`lab/shop/warm_pool.py`](lab/shop/warm_pool.py)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### Too many connections

```sh
# ana@shop-1:~/shop$
python3 rush.py 300
```

### Who holds the connections

```sh
# ana@shop-1:~/shop$
python3 rush.py 300
# root@db:~#
mysql
mysql> SHOW VARIABLES LIKE 'max_connections';
mysql> SELECT user, command, COUNT(*) AS connections FROM performance_schema.processlist WHERE command <> 'Daemon' GROUP BY user, command;
# ana@shop-1:~/shop$
python3 rush.py 300
mysql> SHOW GLOBAL STATUS LIKE 'Max_used_connections';
mysql> SHOW GLOBAL STATUS LIKE 'Connection_errors_max_connections';
mysql> SHOW GLOBAL STATUS LIKE 'Threads_connected';
```

### Why not just raise the limit

```sh
mysql> SET GLOBAL max_connections = 1000;
# ana@shop-1:~/shop$
python3 rush.py 300
```

### Fix 1: a connection pool

```sh
mysql> FLUSH STATUS;
# ana@shop-1:~/shop$
python3 rush.py 300 --pool
mysql> SHOW GLOBAL STATUS LIKE 'Max_used_connections';
```

### Fix 2: pools that fit

```sh
# ana@shop-1:~/shop$
python3 warm_pool.py 60
# ana@shop-2:~/shop$
python3 warm_pool.py 60
# ana@shop-3:~/shop$
python3 warm_pool.py 60
mysql> SELECT SUBSTRING_INDEX(host, ':', 1) AS app, command, COUNT(*) AS connections FROM performance_schema.processlist WHERE user = 'shop' GROUP BY app, command;
mysql> SHOW VARIABLES LIKE 'wait_timeout';
mysql> SELECT SUBSTRING_INDEX(host, ':', 1) AS app, command, COUNT(*) AS connections FROM performance_schema.processlist WHERE user = 'shop' GROUP BY app, command;
mysql> SHOW GLOBAL STATUS LIKE 'Threads_connected';
```

### Keep it from coming back

```sh
mysql> ALTER USER 'shop'@'%' WITH MAX_USER_CONNECTIONS 120;
# ana@shop-1:~/shop$
python3 rush.py 300
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
