# How to Fix Docker Compose Containers That Can't Talk to Each Other

Video: https://youtu.be/J1OC8eJhnmA  
Written version: https://cloudexplainers.com/how-to-fix-docker-compose-containers-that-can-t-talk-to-each-other/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/app/Dockerfile`](lab/app/Dockerfile)
- [`lab/app/report.py`](lab/app/report.py)
- [`lab/app/web.py`](lab/app/web.py)
- [`lab/laptop/Dockerfile`](lab/laptop/Dockerfile)
- [`lab/reports/compose.yaml`](lab/reports/compose.yaml)
- [`lab/shop/compose.yaml`](lab/shop/compose.yaml)
- [`lab/shop/teas.sql`](lab/shop/teas.sql)

## Commands, in the order the video runs them

### Running, but not talking

```sh
# ana@laptop:~/shop$
docker compose logs --no-log-prefix web
docker compose ps -a --format 'table {{.Service}}\t{{.Status}}'
psql -h localhost -p 5433 -U postgres -c 'SELECT count(*) FROM teas'
```

### The usual fix: the service name

```sh
# ana@laptop:~/shop$
grep -n DB_HOST compose.yaml
sed -i 's/DB_HOST: localhost/DB_HOST: db/' compose.yaml
grep -n DB_HOST compose.yaml
docker compose up -d
docker compose logs --no-log-prefix web
curl localhost:8000
```

### Why localhost fails

```sh
# ana@laptop:~/shop$
docker network inspect shop_default --format '{{range .Containers}}{{.Name}} {{.IPv4Address}}{{println}}{{end}}'
docker compose exec web grep nameserver /etc/resolv.conf
docker compose exec web getent hosts db
```

### The port that only works outside

```sh
# ana@laptop:~/shop$
docker compose ps --format 'table {{.Service}}\t{{.Ports}}'
sed -i 's/DB_PORT: "5432"/DB_PORT: "5433"/' compose.yaml
grep -n DB_ compose.yaml
docker compose logs --no-log-prefix web
```

### Two projects, two networks

```sh
# ana@laptop:~/reports$
cat compose.yaml
docker compose run --rm report
docker network ls --filter name=_default
cat compose.yaml
docker compose run --rm report
```

### Works on the second try

```sh
# ana@laptop:~/shop$
docker compose down -v
docker compose up -d
docker compose logs --no-log-prefix web
docker compose logs --no-log-prefix db | grep -E 'init process complete|ready to accept'
docker compose up -d
docker compose logs --no-log-prefix web
grep -A 4 healthcheck compose.yaml
grep -A 2 depends_on compose.yaml
docker compose up -d
docker compose logs --no-log-prefix web
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
