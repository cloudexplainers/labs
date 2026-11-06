# What Happens When You Run a Docker Container

Video: https://youtu.be/zV0fWUH5hMc  
Written version: https://cloudexplainers.com/what-happens-when-you-run-a-docker-container/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### One command, four seconds

```sh
# ana@laptop:~$
time docker run -d --name shop -p 8080:80 --memory 256m nginx:alpine
```

### Who does the work

```sh
# ana@laptop:~$
docker version --format 'client {{.Client.Version}}, server {{.Server.Version}}'
ls -l /var/run/docker.sock
curl -s --unix-socket /var/run/docker.sock http://localhost/containers/json | jq '.[0] | {Names, Image, State}'
```

### The image: layers on disk

```sh
# ana@laptop:~$
docker image ls
docker image ls
docker image inspect nginx:alpine --format '{{len .RootFS.Layers}} layers'
docker info --format '{{.Driver}}'
docker exec shop df -h /
docker exec shop grep PRETTY /etc/os-release
grep PRETTY /etc/os-release
uname -r; docker exec shop uname -r
```

### A container is a process

```sh
# ana@laptop:~$
PID=$(docker inspect --format '{{.State.Pid}}' shop); echo $PID
ps -o pid,user,cmd -p $PID
pstree -s -p $PID
docker exec shop ps -o pid,user,args
docker exec shop hostname
sudo readlink /proc/$$/ns/pid /proc/$PID/ns/pid /proc/$$/ns/net /proc/$PID/ns/net
```

### Limits and a network cable

```sh
# ana@laptop:~$
cat /proc/$PID/cgroup
CG=/sys/fs/cgroup/system.slice/docker-$(docker inspect --format '{{.Id}}' shop).scope
cat $CG/memory.max $CG/memory.current
docker inspect --format '{{.NetworkSettings.Networks.bridge.IPAddress}}' shop
ip -br addr show docker0
ip -br link | grep veth
sudo iptables -t nat -S DOCKER | grep 8080
```

### Stop it, run it again

```sh
# ana@laptop:~$
docker stop shop
ps -p $PID || echo 'no such process'
docker rm shop
time docker run -d --name shop -p 8080:80 --memory 256m nginx:alpine
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
