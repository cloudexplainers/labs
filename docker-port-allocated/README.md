# How to Fix Docker Port Already Allocated Errors

Video: https://youtu.be/lIQrKVh20ZQ  
Written version: https://cloudexplainers.com/how-to-fix-docker-port-already-allocated-errors/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/compose.yaml`](lab/compose.yaml)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### Port already allocated

```sh
# ana@laptop:~$
docker run -d --name shop-v2 -p 8080:80 shop:v2
```

### Who has the port?

```sh
# ana@laptop:~$
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
docker ps --filter publish=8080 --format '{{.Names}}'
curl -s localhost:8080
```

### Free the port

```sh
# ana@laptop:~$
docker stop shop-v1
docker run -d --name shop-v2 -p 8080:80 shop:v2
docker ps -a --format 'table {{.Names}}\t{{.Status}}'
docker rm shop-v2
docker run -d --name shop-v2 -p 8080:80 shop:v2
curl -s localhost:8080
docker rm shop-v1
```

### Behind the port

```sh
# ana@laptop:~$
sudo ss -ltnp 'sport = :8080'
pgrep -a docker-proxy
```

### When it isn't a container

```sh
# ana@laptop:~$
python3 -m http.server 8081
docker run -d --name shop-test -p 8081:80 shop:v2
docker ps --filter publish=8081 --format '{{.Names}}'
sudo ss -ltnp 'sport = :8081'
lsof -nP -i :8081
python3 -m http.server 8081
docker rm shop-test
docker run -d --name shop-test -p 8081:80 shop:v2
docker ps --format 'table {{.Names}}\t{{.Ports}}'
```

### The same fix in Compose

```sh
# ana@laptop:~/shop$
cat compose.yaml
docker compose up -d
cat compose.yaml
docker compose up -d
docker compose ps --format 'table {{.Name}}\t{{.Ports}}'
curl -s localhost:8082
docker compose down
ss -ltn 'sport = :8082'
```

### Never again

```sh
# ana@laptop:~$
docker run -d --name shop-try -p 80 shop:v2
docker port shop-try
curl -s localhost:32768
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
