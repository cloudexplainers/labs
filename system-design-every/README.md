# Every System Design Concept You Need, in One Diagram

Video: https://youtu.be/A_zwj_CNm7E  
Written version: https://cloudexplainers.com/every-system-design-concept-you-need-in-one-diagram/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Commands, in the order the video runs them

### DNS

```sh
dig @1.1.1.1 wikipedia.org
```

### Load balancer

```sh
for i in 1 2 3 4 5 6; do curl -s localhost:8088 | grep Hostname; done
docker stop server-2
for i in 1 2 3 4 5 6; do curl -s localhost:8088 | grep Hostname; done
for i in $(seq 1 100); do curl -s -o /dev/null -w '%{http_code}\n' localhost:8088; done | sort | uniq -c
```

### Database & index

```sh
EXPLAIN ANALYZE SELECT * FROM orders WHERE customer_id = 4242;
CREATE INDEX orders_customer_idx ON orders (customer_id);
EXPLAIN ANALYZE SELECT * FROM orders WHERE customer_id = 4242;
```

### Cache

```sh
python3 cache.py
redis-cli TTL top_products
```

### Replication

```sh
primary=# SELECT application_name, state, sync_state FROM pg_stat_replication;
primary=# INSERT INTO accounts VALUES (3, 'cleo', 75);
replica=# SELECT * FROM accounts;
replica=# INSERT INTO accounts VALUES (4, 'dev', 10);
docker stop primary
replica=# SELECT pg_promote();
new primary=# INSERT INTO accounts VALUES (4, 'dev', 10);
```

### Sharding

```sh
python3 shard.py
```

### Message queue

```sh
python3 signup.py
python3 worker.py
```

### CDN

```sh
curl -s -D - -o /dev/null https://cdn.jsdelivr.net/npm/react@18.3.1/umd/react.production.min.js
curl -s -o /dev/null -w 'first byte: %{time_starttransfer}s' https://cdn.jsdelivr.net/npm/react@18.3.1/umd/react.production.min.js
```

### Monitoring

```sh
python3 latency_report.py
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
