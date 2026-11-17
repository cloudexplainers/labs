# Docker: Full Tutorial for Beginners

Video: https://youtu.be/kxdr7tcZnoo  
Written version: https://cloudexplainers.com/docker-full-tutorial-for-beginners/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/laptop/Dockerfile`](lab/laptop/Dockerfile)
- [`lab/steps/s1/Dockerfile`](lab/steps/s1/Dockerfile)
- [`lab/steps/s1/app.py`](lab/steps/s1/app.py)
- [`lab/steps/s1/requirements.txt`](lab/steps/s1/requirements.txt)
- [`lab/steps/s2/app.py`](lab/steps/s2/app.py)
- [`lab/steps/s3/app.py`](lab/steps/s3/app.py)
- [`lab/steps/s4/Dockerfile`](lab/steps/s4/Dockerfile)
- [`lab/steps/s5/app.py`](lab/steps/s5/app.py)
- [`lab/steps/s6/app.py`](lab/steps/s6/app.py)
- [`lab/steps/s6/compose.yaml`](lab/steps/s6/compose.yaml)
- [`lab/steps/s6/init.sql`](lab/steps/s6/init.sql)
- [`lab/steps/s7/app.py`](lab/steps/s7/app.py)
- [`lab/steps/s8/compose.yaml`](lab/steps/s8/compose.yaml)

## Commands, in the order the video runs them

### One command, a whole app

```sh
# ana@studio-laptop:~/studio$
time docker compose up -d
```

### What Docker is

```sh
# ana@studio-laptop:~$
docker version
```

### Your first container

```sh
# ana@studio-laptop:~$
docker run hello-world
docker ps
cat ~/.docker/config.json
docker ps -a
docker run -it --rm --hostname sandbox ubuntu:24.04 bash
# root@sandbox:/#
whoami
ls /
exit
# ana@studio-laptop:~$
docker ps -a
```

### A web server and its port

```sh
# ana@studio-laptop:~$
docker pull nginx:alpine
docker images
docker run -d --name web nginx:alpine
docker ps
curl localhost:8080
docker rm -f web
docker run -d --name web -p 8080:80 nginx:alpine
docker ps
curl -s localhost:8080 | grep title
docker logs web
```

### Inside a container

```sh
# ana@studio-laptop:~$
grep PRETTY /etc/os-release
uname -r
docker exec -it web sh
/ # grep PRETTY /etc/os-release
/ # uname -r
/ # ps
/ # echo '<h1>Willow Yoga</h1>' > /usr/share/nginx/html/index.html
/ # exit
# ana@studio-laptop:~$
curl -s localhost:8080
docker rm -f web
docker run -d --name web -p 8080:80 nginx:alpine
curl -s localhost:8080 | grep title
docker stop web
docker ps -a
docker rm web
```

### Containers that come back

```sh
# ana@studio-laptop:~$
docker run -d --name always --restart unless-stopped nginx:alpine
docker run -d --name plain nginx:alpine
sudo systemctl restart docker
docker ps -a
docker rm -f always plain
```

### Your own image: a Dockerfile

```sh
# ana@studio-laptop:~$
cd studio
# ana@studio-laptop:~/studio$
ls
cat app.py
cat requirements.txt
cat Dockerfile
time docker build -t yoga-web .
docker run -d --name yoga -p 8000:8000 yoga-web
curl localhost:8000
docker logs yoga
time docker build -t yoga-web .
docker rm -f yoga
docker run -d --name yoga -p 8000:8000 yoga-web
curl -s localhost:8000
docker logs yoga
```

### Fast rebuilds: the layer cache

```sh
# ana@studio-laptop:~/studio$
time docker build -t yoga-web .
cat Dockerfile
time docker build -t yoga-web .
docker images yoga-web
```

### Keep files out: .dockerignore

```sh
# ana@studio-laptop:~/studio$
ls
du -sh photos
time docker build -t yoga-web .
docker images yoga-web
cat .dockerignore
time docker build -t yoga-web .
docker images yoga-web
```

### Edit without rebuilding: bind mounts

```sh
# ana@studio-laptop:~/studio$
docker run -d --name dev -p 8000:8000 -v "$PWD":/app yoga-web flask --app app run --host 0.0.0.0 --port 8000 --debug
curl -s localhost:8000
docker logs dev 2>&1 | tail -n 4
curl -s localhost:8000
docker rm -f dev
```

### Share an image: registries

```sh
# ana@studio-laptop:~/studio$
docker run -d --name registry -p 5000:5000 registry:2
docker tag yoga-web localhost:5000/yoga-web:1.0
docker push localhost:5000/yoga-web:1.0
docker image rm localhost:5000/yoga-web:1.0
docker pull localhost:5000/yoga-web:1.0
docker rm -f -v registry
```

### Data that survives: volumes

```sh
# ana@studio-laptop:~/studio$
docker run -d --name db -e POSTGRES_PASSWORD=yoga-lab-only postgres:17-alpine
docker exec db psql -U postgres -c "CREATE TABLE classes (start text, name text)"
docker rm -f db
docker run -d --name db -e POSTGRES_PASSWORD=yoga-lab-only postgres:17-alpine
docker exec db psql -U postgres -c "SELECT * FROM classes"
docker run -d --name db -e POSTGRES_PASSWORD=yoga-lab-only -v studio-data:/var/lib/postgresql/data postgres:17-alpine
cat init.sql
docker exec -i db psql -U postgres < init.sql
docker rm -f db
docker run -d --name db -e POSTGRES_PASSWORD=yoga-lab-only -v studio-data:/var/lib/postgresql/data postgres:17-alpine
docker exec db psql -U postgres -c "SELECT * FROM classes"
docker volume ls
```

### Containers talking: networks

```sh
# ana@studio-laptop:~/studio$
cat app.py
docker build -q -t yoga-web .
docker run -d --name yoga -p 8000:8000 -e DATABASE_URL=postgresql://postgres:yoga-lab-only@localhost/postgres yoga-web
curl -s localhost:8000 | grep title
docker logs yoga 2>&1 | grep OperationalError
docker network create studio-net
docker network connect studio-net db
docker rm -f yoga
docker run -d --name yoga -p 8000:8000 --network studio-net -e DATABASE_URL=postgresql://postgres:yoga-lab-only@db/postgres yoga-web
curl -s localhost:8000
docker exec yoga getent hosts db
```

### Docker Compose: one file

```sh
# ana@studio-laptop:~/studio$
cat compose.yaml
docker rm -f yoga db
docker compose up -d
docker ps
curl -s localhost:8000
docker compose exec db psql -U postgres -c "INSERT INTO classes VALUES ('20:00', 'Candlelight flow')"
docker compose down
docker volume ls
docker compose up -d
curl -s localhost:8000
docker compose logs web --tail 2
docker stats --no-stream
```

### Two errors you will meet

```sh
# ana@studio-laptop:~/studio$
docker run -d --name extra -p 8000:8000 yoga-web
docker ps -a
docker rm extra
docker run yogaweb
```

### Why it took ten seconds

```sh
# ana@studio-laptop:~/studio$
docker compose exec web cat /proc/1/comm
grep -n init: compose.yaml
docker compose exec web cat /proc/1/comm
time docker compose down
```

### Cleaning up

```sh
# ana@studio-laptop:~/studio$
docker system df
docker compose down -v
docker image prune -a -f
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
