# Redis: Full Tutorial for Beginners

Video: https://youtu.be/2IlDbfPYmIM  
Written version: https://cloudexplainers.com/redis-full-tutorial-for-beginners/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/app/jobs_v1.py`](lab/app/jobs_v1.py)
- [`lab/app/jobs_v2.py`](lab/app/jobs_v2.py)
- [`lab/app/make_db.py`](lab/app/make_db.py)
- [`lab/app/photos.py`](lab/app/photos.py)
- [`lab/app/price.py`](lab/app/price.py)
- [`lab/app/worker.py`](lab/app/worker.py)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### A garage's job board

```sh
127.0.0.1:6379> HSET job:1007 car "2019 Ford F-150" owner Sam status waiting
127.0.0.1:6379> LPUSH jobs 1007
garage:6379> BRPOP jobs 0
garage:6379> HGETALL job:1007
```

### Installing Redis

```sh
# linda@garage:~$
redis-cli ping
sudo apt install -y redis-server
systemctl is-active redis-server
redis-server --version
redis-cli ping
```

### Keys, strings and counters

```sh
# linda@garage:~$
redis-cli
127.0.0.1:6379> SET job:1001:status waiting
127.0.0.1:6379> GET job:1001:status
127.0.0.1:6379> GET job:1002:status
127.0.0.1:6379> SET job:1001:status "in bay 2"
127.0.0.1:6379> GET job:1001:status
127.0.0.1:6379> INCR cars:today
127.0.0.1:6379> INCR cars:today
127.0.0.1:6379> INCR cars:today
127.0.0.1:6379> GET cars:today
127.0.0.1:6379> DEL job:1001:status
127.0.0.1:6379> EXISTS job:1001:status
127.0.0.1:6379> SET bay:2 rob NX EX 30
127.0.0.1:6379> SET bay:2 sam NX EX 30
127.0.0.1:6379> GET bay:2
```

### Keys that expire

```sh
127.0.0.1:6379> SET quote:1001 "brakes: $340" EX 20
127.0.0.1:6379> TTL quote:1001
127.0.0.1:6379> GET quote:1001
127.0.0.1:6379> TTL quote:1001
127.0.0.1:6379> GET quote:1001
127.0.0.1:6379> TTL cars:today
127.0.0.1:6379> INCR quotes:pat
127.0.0.1:6379> EXPIRE quotes:pat 60
127.0.0.1:6379> INCR quotes:pat
127.0.0.1:6379> INCR quotes:pat
127.0.0.1:6379> INCR quotes:pat
127.0.0.1:6379> TTL quotes:pat
```

### Hashes: one key, many fields

```sh
127.0.0.1:6379> HSET job:1001 car "2015 Honda Civic" owner Pat status waiting
127.0.0.1:6379> HGET job:1001 car
127.0.0.1:6379> HGETALL job:1001
127.0.0.1:6379> HINCRBY job:1001 hours 2
127.0.0.1:6379> HSET session:7f3a9c user linda role front-desk
127.0.0.1:6379> EXPIRE session:7f3a9c 1800
127.0.0.1:6379> TTL session:7f3a9c
127.0.0.1:6379> HGETALL session:7f3a9c
127.0.0.1:6379> GET job:1001
127.0.0.1:6379> TYPE job:1001
```

### Lists: a queue of jobs

```sh
127.0.0.1:6379> LPUSH jobs 1001 1002 1003
127.0.0.1:6379> LRANGE jobs 0 -1
127.0.0.1:6379> RPOP jobs
127.0.0.1:6379> LLEN jobs
127.0.0.1:6379> LPUSH log "08:02 Civic in bay 1" "08:15 F-150 in bay 2" "08:40 RAV4 waiting" "09:05 Civic done"
127.0.0.1:6379> LTRIM log 0 2
127.0.0.1:6379> LRANGE log 0 -1
# rob@garage:~$
redis-cli
127.0.0.1:6379> BRPOP jobs 0
127.0.0.1:6379> BRPOP jobs 0
127.0.0.1:6379> BRPOP jobs 0
127.0.0.1:6379> LPUSH jobs 1004
127.0.0.1:6379> SUBSCRIBE garage:ready
127.0.0.1:6379> PUBLISH garage:ready "job 1001: Civic ready for pickup"
127.0.0.1:6379> PUBLISH garage:ready "job 1002: brakes done"
```

### Sets and sorted sets

```sh
127.0.0.1:6379> SADD parts:1001 "brake pads" rotors "brake fluid"
127.0.0.1:6379> SADD shelf "brake pads" "oil filter" "wiper blades"
127.0.0.1:6379> SADD shelf "oil filter"
127.0.0.1:6379> SDIFF parts:1001 shelf
127.0.0.1:6379> SISMEMBER shelf rotors
127.0.0.1:6379> ZADD done:week 4 rob 6 sam 3 maria
127.0.0.1:6379> ZINCRBY done:week 1 rob
127.0.0.1:6379> ZREVRANGE done:week 0 -1 WITHSCORES
127.0.0.1:6379> KEYS *
127.0.0.1:6379> SCAN 0 MATCH job:* COUNT 100
127.0.0.1:6379> MULTI
127.0.0.1:6379(TX)> HSET job:1001 status done
127.0.0.1:6379(TX)> ZINCRBY done:week 1 rob
127.0.0.1:6379(TX)> EXEC
```

### Surviving a restart and a crash

```sh
127.0.0.1:6379> CONFIG GET save
127.0.0.1:6379> CONFIG GET appendonly
# linda@garage:~$
sudo systemctl restart redis-server
redis-cli GET cars:today
redis-cli SET job:1005:status waiting
sudo kill -9 $(pidof redis-server)
systemctl is-active redis-server
redis-cli GET job:1005:status
redis-cli GET cars:today
redis-cli CONFIG SET appendonly yes
sudo grep -n '^appendonly' /etc/redis/redis.conf
sudo ls /var/lib/redis/appendonlydir
redis-cli SET job:1006:status waiting
sudo kill -9 $(pidof redis-server)
redis-cli GET job:1006:status
```

### Redis from Python

```sh
# linda@garage:~$
python3 -m venv .venv
.venv/bin/pip install redis
cat jobs.py
.venv/bin/python jobs.py
grep -n decode_responses jobs.py
.venv/bin/python jobs.py
cat price.py
.venv/bin/python price.py
.venv/bin/python price.py
redis-cli TTL price:rotors
# rob@garage:~$
cat worker.py
# linda@garage:~$
redis-cli LPUSH jobs 1008 1009
# rob@garage:~$
.venv/bin/python worker.py
```

### When memory runs out

```sh
# linda@garage:~$
redis-cli CONFIG GET maxmemory
redis-cli CONFIG GET maxmemory-policy
redis-cli CONFIG SET maxmemory 3mb
cat photos.py
.venv/bin/python photos.py
redis-cli CONFIG SET maxmemory-policy allkeys-lru
.venv/bin/python photos.py
redis-cli EXISTS job:1001
redis-cli EXISTS cars:today
127.0.0.1:6379> INFO memory
```

### Other PCs and a password

```sh
# rob@bay:~$
redis-cli -h garage ping
# linda@garage:~$
sudo grep -n '^bind\|^protected-mode' /etc/redis/redis.conf
sudo grep -n '^bind' /etc/redis/redis.conf
sudo systemctl restart redis-server
# rob@bay:~$
redis-cli -h garage ping
# linda@garage:~$
sudo grep -n '^requirepass' /etc/redis/redis.conf
sudo systemctl restart redis-server
# rob@bay:~$
redis-cli -h garage ping
redis-cli -h garage --askpass
garage:6379> PING
127.0.0.1:6379> ACL SETUSER bay on >bay-only-9 ~jobs ~job:* +brpop +hgetall +ping
# rob@bay:~$
redis-cli -h garage --user bay --askpass
garage:6379> PING
garage:6379> DEL jobs
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
