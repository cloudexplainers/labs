# How to Fix Docker 'Permission Denied' on docker.sock

Video: https://youtu.be/MB9C3YlbBwI  
Written version: https://cloudexplainers.com/how-to-fix-docker-permission-denied-on-docker-sock/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/laptop/Dockerfile`](lab/laptop/Dockerfile)

## Commands, in the order the video runs them

### Permission denied on docker.sock

```sh
# ben@office-pc:~$
docker ps --format '{{.Names}}  {{.Image}}  {{.Status}}'
sudo docker ps --format '{{.Names}}  {{.Image}}  {{.Status}}'
```

### The fix: the docker group

```sh
# ben@office-pc:~$
id
sudo usermod -aG docker ben
docker ps --format '{{.Names}}  {{.Image}}  {{.Status}}'
```

### Why it still fails: log in again

```sh
# ben@office-pc:~$
id ben
getent group docker
id
newgrp docker
docker ps --format '{{.Names}}  {{.Image}}  {{.Status}}'
exit
id
docker ps --format '{{.Names}}  {{.Image}}  {{.Status}}'
```

### Denied, or not running?

```sh
# ana@office-pc:~$
sudo systemctl stop docker docker.socket
# ben@office-pc:~$
docker ps --format '{{.Names}}  {{.Image}}  {{.Status}}'
sudo docker ps --format '{{.Names}}  {{.Image}}  {{.Status}}'
```

### Two fixes that backfire

```sh
# ana@office-pc:~$
id eli
sudo usermod -G docker eli
id eli
sudo usermod -aG sudo eli
id eli
sudo chmod 666 /var/run/docker.sock
ls -l /var/run/docker.sock
# cara@office-pc:~$
docker ps --format '{{.Names}}  {{.Image}}  {{.Status}}'
docker ps --format '{{.Names}}  {{.Image}}  {{.Status}}'
sudo ls /root
# ana@office-pc:~$
sudo reboot
ls -l /var/run/docker.sock
systemctl cat docker.socket
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
