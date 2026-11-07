# How Redis Caching Works

Video: https://youtu.be/vSlS72wiP5o  
Written version: https://cloudexplainers.com/how-redis-caching-works/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/schema.sql`](lab/schema.sql)
- [`lab/shop.py`](lab/shop.py)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### The same slow answer

```sh
# ana@laptop:~/shop$
python3 shop.py bestsellers --no-cache
python3 shop.py bestsellers --no-cache
```

### What Redis is

```sh
# ana@laptop:~/shop$
redis-cli -h cache PING
redis-cli -h cache SET greeting hello
redis-cli -h cache GET greeting
redis-cli -h cache GET nothing-here
```

### Ask the cache first

```sh
# ana@laptop:~/shop$
python3 shop.py bestsellers
python3 shop.py bestsellers
```

### Answers that expire

```sh
# ana@laptop:~/shop$
redis-cli -h cache TTL shop:bestsellers
python3 shop.py bestsellers
```

### When the copy is wrong

```sh
# ana@laptop:~/shop$
python3 shop.py price 3
python3 shop.py set-price 3 11.50
python3 shop.py price 3
redis-cli -h cache TTL shop:product:3
python3 shop.py set-price 3 11.50 --clear-cache
python3 shop.py price 3
```

### When memory runs out

```sh
# ana@laptop:~/shop$
redis-cli -h cache CONFIG GET maxmemory
redis-cli -h cache CONFIG GET maxmemory-policy
python3 shop.py fill 40000
redis-cli -h cache INFO memory | grep used_memory_human
redis-cli -h cache CONFIG SET maxmemory-policy allkeys-lru
python3 shop.py fill 40000
redis-cli -h cache INFO stats | grep evicted_keys
redis-cli -h cache EXISTS shop:page:1
redis-cli -h cache EXISTS shop:page:40000
```

### Fifty visitors at once

```sh
# ana@laptop:~/shop$
python3 shop.py rush 50
python3 shop.py rush 50 --lock
```

### Caching in real life

```sh
# ana@laptop:~/shop$
redis-cli -h cache FLUSHALL
python3 shop.py bestsellers
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
