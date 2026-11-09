# Docker vs Docker Compose: Which One Should You Use?

Video: https://youtu.be/46aVYNUZxJA  
Written version: https://cloudexplainers.com/docker-vs-docker-compose-which-one-should-you-use/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/shop/Dockerfile`](lab/shop/Dockerfile)
- [`lab/shop/app.py`](lab/shop/app.py)
- [`lab/shop/compose.yaml`](lab/shop/compose.yaml)
- [`lab/stage/README.md`](lab/stage/README.md)
- [`lab/stage/compose.first.yaml`](lab/stage/compose.first.yaml)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### One shop, two ways to start it

```sh
# ana@laptop:~/shop$
docker run -d --name db -e POSTGRES_PASSWORD=tea-lab-only -v dbdata:/var/lib/postgresql postgres:18-alpine
docker network create shop-net
docker run -d --name app --network shop-net -p 8080:8000 -e DB_HOST=db -e DB_PASSWORD=tea-lab-only shop-app
docker compose up -d
```

### Starting it by hand

```sh
# ana@laptop:~/shop$
docker build -q -t shop-app .
docker run -d --name app -p 8080:8000 -e DB_HOST=db -e DB_PASSWORD=tea-lab-only shop-app
docker ps -a --format 'table {{.Names}}\t{{.Status}}'
docker logs app 2>&1 | tail -1
docker network connect shop-net db
docker rm app
curl localhost:8080
for i in 1 2 3; do curl -s -X POST localhost:8080/order; done
curl localhost:8080
docker run -d --name db -e POSTGRES_PASSWORD=tea-lab-only -v dbdata:/var/lib/postgresql postgres:18-alpine
```

### The same shop in one file

```sh
# ana@laptop:~/shop$
cat compose.yaml
docker compose version
docker-compose version
docker compose up -d
```

### Started is not ready

```sh
# ana@laptop:~/shop$
docker compose ps -a --format 'table {{.Service}}\t{{.Status}}'
docker compose logs app | tail -2
cat compose.yaml
curl localhost:8080
for i in 1 2 3; do curl -s -X POST localhost:8080/order; done
curl localhost:8080
```

### Is it a different Docker?

```sh
# ana@laptop:~/shop$
docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}'
docker inspect shop-app-1 --format '{{index .Config.Labels "com.docker.compose.project"}}'
```

### Run it again, change one line

```sh
# ana@laptop:~/shop$
docker compose up -d
sed -i 's/8080:8000/8081:8000/' compose.yaml && grep 8081 compose.yaml
docker compose up -d
curl localhost:8081
```

### Tearing it all down

```sh
# ana@laptop:~/shop$
docker compose down
docker ps -a --format '{{.Names}}' | wc -l
docker volume ls --format '{{.Name}}'
docker compose up -d
curl localhost:8081
docker compose down -v
```

### Where plain docker is simpler

```sh
# ana@laptop:~/shop$
docker run --rm python:3.13-slim python --version
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
