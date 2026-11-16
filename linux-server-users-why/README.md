# Why One Linux Server Handles More Users Than You Think

Video: https://youtu.be/ihjUGWSCvD4  
Written version: https://cloudexplainers.com/why-one-linux-server-handles-more-users-than-you-think/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/cpuused`](lab/cpuused)
- [`lab/idle.py`](lab/idle.py)
- [`lab/market/app.py`](lab/market/app.py)
- [`lab/market/make_db.py`](lab/market/make_db.py)
- [`lab/market/market.service`](lab/market/market.service)
- [`lab/market/nginx.conf`](lab/market/nginx.conf)
- [`lab/market/www/index.html`](lab/market/www/index.html)
- [`lab/memused`](lab/memused)
- [`lab/payments.py`](lab/payments.py)
- [`lab/payments.service`](lab/payments.service)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### One core, a flood of requests

```sh
# ana@market:~$
nproc
# ana@laptop:~$
wrk -t2 -c50 -d10s http://market/
```

### Real code, same core

```sh
# ana@laptop:~$
wrk -t2 -c10 -d10s http://market/api/stalls
```

### Open tabs cost almost nothing

```sh
# ana@market:~$
memused
# ana@laptop:~$
python3 idle.py 5000 40
# ana@market:~$
ss -s
memused
```

### When it's full, a line forms

```sh
# ana@laptop:~$
wrk -t2 -c400 -d10s http://market/api/stalls
# ana@market:~$
cpuused 3
```

### The slowest step sets the limit

```sh
# ana@laptop:~$
wrk -t2 -c20 -d10s "http://market/api/orders?customer=1234"
# ana@market:/srv/market$
sqlite3 market.db "EXPLAIN QUERY PLAN SELECT * FROM orders WHERE customer_id = 1234"
time sqlite3 market.db "CREATE INDEX orders_by_customer ON orders(customer_id)"
sqlite3 market.db "EXPLAIN QUERY PLAN SELECT * FROM orders WHERE customer_id = 1234"
# ana@laptop:~$
wrk -t2 -c20 -d10s "http://market/api/orders?customer=1234"
```

### Full, with the core asleep

```sh
# ana@laptop:~$
wrk -t2 -c50 -d10s --timeout 30s -s post.lua http://market/api/checkout
# ana@market:/srv/market$
cpuused 3
sudo systemctl daemon-reload && sudo systemctl restart market
# ana@laptop:~$
wrk -t2 -c50 -d10s --timeout 30s -s post.lua http://market/api/checkout
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
