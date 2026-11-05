# The 7 Levels of Docker

Video: https://youtu.be/015x1lT4cWU  
Written version: https://cloudexplainers.com/the-7-levels-of-docker/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/counter/Dockerfile`](lab/counter/Dockerfile)
- [`lab/counter/app.py`](lab/counter/app.py)
- [`lab/counter/compose.yaml`](lab/counter/compose.yaml)
- [`lab/counter/requirements.txt`](lab/counter/requirements.txt)
- [`lab/go-hello/Dockerfile`](lab/go-hello/Dockerfile)
- [`lab/go-hello/Dockerfile.big`](lab/go-hello/Dockerfile.big)
- [`lab/go-hello/main.go`](lab/go-hello/main.go)
- [`lab/hello/Dockerfile`](lab/hello/Dockerfile)
- [`lab/hello/app.py`](lab/hello/app.py)
- [`lab/hello/requirements.txt`](lab/hello/requirements.txt)

## Commands, in the order the video runs them

### The 7 levels

```sh
# ana@laptop:~$
docker run -d -p 8080:80 --name web nginx:1.31-alpine
curl -s localhost:8080 | grep title
```

### Level 1: Containers

```sh
# ana@laptop:~$
docker run hello-world
head -2 /etc/os-release
docker run --rm ubuntu:24.04 head -2 /etc/os-release
uname -r
docker run --rm ubuntu:24.04 uname -r
docker run --rm alpine:3.24 ps
```

### Level 2: Images

```sh
# ana@laptop:~$
docker pull nginx:1.31-alpine
docker run -d --name web1 nginx:1.31-alpine
docker run -d --name web2 nginx:1.31-alpine
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Ports}}"
```

### Level 3: Ports

```sh
# ana@laptop:~$
curl localhost:8080
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Ports}}"
```

### Level 4: Build your own

```sh
# ana@laptop:~/hello$
cat Dockerfile
docker build -t hello-app .
sed -i 's/from a container/from my own image/' app.py
docker build -t hello-app .
docker run -d -p 8000:8000 --name hello hello-app
curl localhost:8000
```

### Level 5: Volumes

```sh
# ana@laptop:~$
docker run --name box alpine:3.24 sh -c 'echo first note > /note.txt'
docker rm box
docker run --rm alpine:3.24 cat /note.txt
docker volume create notes
docker run --rm -v notes:/data alpine:3.24 sh -c 'echo first note > /data/note.txt'
docker run --rm -v notes:/data alpine:3.24 cat /data/note.txt
```

### Level 6: Compose

```sh
# ana@laptop:~/counter$
cat compose.yaml
docker compose up -d
curl localhost:8000
curl localhost:8000
docker compose down
docker compose up -d
curl localhost:8000
```

### Level 7: Small, safe images

```sh
# ana@laptop:~/go-hello$
cat Dockerfile.big
cat Dockerfile
docker image ls hello-go
docker run --rm hello-go:big
docker run --rm hello-go:small
docker run --rm hello-go:big whoami
docker run --rm hello-go:small whoami
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
