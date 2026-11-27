# What Happens When You Install Docker on Ubuntu

Video: https://youtu.be/5vUYI6gDY1Y  
Written version: https://cloudexplainers.com/what-happens-when-you-install-docker-on-ubuntu/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/index.html`](lab/index.html)

## Commands, in the order the video runs them

### One install, four new things

```sh
# mary@gameserver:~$
docker --version
```

### Docker's own repository

```sh
# mary@gameserver:~$
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
head -3 /etc/apt/keyrings/docker.asc
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF
# mary@gameserver:~$
sudo apt update
apt-cache policy docker-ce | head -4
```

### The install

```sh
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

### What it added

```sh
# mary@gameserver:~$
systemctl status docker --no-pager --lines=0
systemctl is-enabled docker.service docker.socket containerd.service
ps -eo user,pid,cmd | grep -E 'dockerd|containerd' | grep -v grep
ls -l /var/run/docker.sock
getent group docker
ip -br addr show docker0
sudo iptables -S FORWARD | head -2
sudo ls /var/lib/docker
sudo du -sh /var/lib/docker /usr/bin/dockerd /usr/bin/containerd /usr/bin/docker
```

### Permission denied

```sh
# mary@gameserver:~$
docker run hello-world
sudo usermod -aG docker mary
groups
groups
```

### The first container

```sh
docker run -d --name signups --restart unless-stopped -p 8080:80 -v ~/signups:/usr/share/nginx/html:ro nginx
# mary@gameserver:~$
sudo du -sh /var/lib/docker
curl -s localhost:8080 | grep Signed
ip -br link | grep -E 'docker0|veth'
```

### The firewall surprise

```sh
# mary@gameserver:~$
sudo ufw status
# jim@laptop:~$
curl -s -m 3 gameserver:8000 || echo 'no answer'
curl -s -m 3 gameserver:8080 | grep Signed
# mary@gameserver:~$
sudo iptables -t nat -S DOCKER
docker rm -f signups
docker run -d --name signups --restart unless-stopped -p 127.0.0.1:8080:80 -v ~/signups:/usr/share/nginx/html:ro nginx
# jim@laptop:~$
curl -s -m 3 gameserver:8080 || echo 'no answer'
# mary@gameserver:~$
curl -s localhost:8080 | grep Signed
```

### After a restart

```sh
# mary@gameserver:~$
uptime -p
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
curl -s localhost:8080 | grep Signed
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
