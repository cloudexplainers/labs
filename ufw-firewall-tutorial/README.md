# Linux Firewall with ufw: Full Tutorial for Beginners

Video: https://youtu.be/e8ycU4HXtFs  
Written version: https://cloudexplainers.com/linux-firewall-with-ufw-full-tutorial-for-beginners/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/shop/bays.py`](lab/shop/bays.py)
- [`lab/shop/bays.service`](lab/shop/bays.service)
- [`lab/shop/www/index.html`](lab/shop/www/index.html)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### Locked out by one command

```sh
# beth@home:~$
ssh shop
# beth@shop:~$
sudo ufw enable
hostname
exit
# beth@home:~$
ssh shop
# guest@phone:~$
curl -sS -m 10 -o /dev/null -w '%{http_code}\n' shop
```

### Back in, from the server's own screen

```sh
# beth@shop:~$
sudo ufw status verbose
sudo ss -tln | grep -v 127.0.0
sudo ufw allow OpenSSH
# beth@home:~$
ssh shop
# beth@shop:~$
hostname
```

### Opening ports for programs

```sh
# beth@shop:~$
sudo ufw app list
sudo ufw app info 'Nginx HTTP'
sudo ufw allow 'Nginx HTTP'
# guest@phone:~$
curl -sS -m 10 -o /dev/null -w '%{http_code}\n' shop
# beth@shop:~$
cat /etc/ufw/applications.d/bays
sudo ufw app list
sudo ufw app info Bays
```

### Only from the shop's network

```sh
# guest@phone:~$
nc -zv -w 10 shop 5000
# dave@office:~$
nc -zv -w 10 shop 5000
# beth@shop:~$
ip -br -4 addr | grep eth
sudo ufw allow from 192.168.50.0/24 to any port 5000 proto tcp
# dave@office:~$
curl -sS -m 10 shop:5000
# guest@phone:~$
nc -zv -w 10 shop 5000
# beth@shop:~$
sudo ufw status numbered
```

### Deny or reject

```sh
# beth@shop:~$
sudo ufw reject 5000/tcp
# guest@phone:~$
nc -zv -w 10 shop 5000
# dave@office:~$
curl -sS -m 10 shop:5000
# beth@shop:~$
sudo ufw status numbered
```

### Rule order: the first match wins

```sh
# guest@stranger:~$
curl -sS -m 10 -o /dev/null -w '%{http_code}\n' shop
# beth@shop:~$
sudo ufw deny from 203.0.113.66
# guest@stranger:~$
curl -sS -m 10 -o /dev/null -w '%{http_code}\n' shop
# beth@shop:~$
sudo ufw status numbered
sudo ufw delete 5
sudo ufw insert 1 deny from 203.0.113.66
# guest@stranger:~$
curl -sS -m 10 -o /dev/null -w '%{http_code}\n' shop
# guest@phone:~$
curl -sS -m 10 -o /dev/null -w '%{http_code}\n' shop
# beth@shop:~$
sudo ufw status numbered
```

### Deleting rules

```sh
# beth@shop:~$
sudo ufw delete deny from 203.0.113.66
sudo ufw status numbered
```

### Limit: too many tries in a row

```sh
# guest@stranger:~$
for i in 1 2 3 4 5 6 7 8; do nc -z -w 3 shop 22 2>/dev/null && echo "try $i: open" || echo "try $i: blocked"; done
# beth@shop:~$
sudo ufw limit OpenSSH
# guest@stranger:~$
for i in 1 2 3 4 5 6 7 8; do nc -z -w 3 shop 22 2>/dev/null && echo "try $i: open" || echo "try $i: blocked"; done
# beth@home:~$
ssh shop
# beth@shop:~$
hostname
```

### Reading the firewall's log

```sh
# guest@phone:~$
nc -zv -w 3 shop 8443
# beth@shop:~$
sudo ufw status verbose | head -3
sudo tail -n 1 /var/log/ufw.log | grep -oE 'UFW BLOCK|IN=\S+|SRC=\S+|DST=\S+|PROTO=\S+|DPT=\S+'
sudo grep -c 'UFW BLOCK' /var/log/ufw.log
```

### Why every rule shows up twice

```sh
# beth@shop:~$
grep IPV6 /etc/default/ufw
```

### Outgoing rules

```sh
# beth@shop:~$
curl -sS -m 5 -o /dev/null -w '%{http_code}\n' http://archive.ubuntu.com/ubuntu/
sudo ufw default deny outgoing
curl -sS -m 5 -o /dev/null -w '%{http_code}\n' http://archive.ubuntu.com/ubuntu/
sudo ufw allow out 80/tcp
curl -sS -m 5 -o /dev/null -w '%{http_code}\n' http://archive.ubuntu.com/ubuntu/
sudo ufw default allow outgoing
```

### Docker's published ports

```sh
# beth@shop:~$
sudo docker run -d --name parts -p 8080:80 nginx:alpine
sudo ufw status | grep -c 8080
# guest@phone:~$
curl -sS -m 10 -o /dev/null -w '%{http_code}\n' shop:8080
# beth@shop:~$
sudo ufw deny 8080/tcp
# guest@phone:~$
curl -sS -m 10 -o /dev/null -w '%{http_code}\n' shop:8080
# beth@shop:~$
sudo docker ps --format '{{.Names}}  {{.Ports}}'
sudo iptables -S FORWARD | head -4
sudo docker rm -f parts
sudo docker run -d --name parts -p 192.168.50.10:8080:80 nginx:alpine
# dave@office:~$
curl -sS -m 10 -o /dev/null -w '%{http_code}\n' shop:8080
# guest@phone:~$
curl -sS -m 10 -o /dev/null -w '%{http_code}\n' shop:8080
```

### Under the hood, and after a restart

```sh
# beth@shop:~$
sudo iptables -S ufw-user-input | head -6
sudo iptables -S ufw-before-input | grep ESTABLISHED
grep ENABLED /etc/ufw/ufw.conf
systemctl status ufw --no-pager | head -4
sudo ufw status
# guest@phone:~$
curl -sS -m 10 -o /dev/null -w '%{http_code}\n' shop
```

### Starting over, the safe way round

```sh
# beth@shop:~$
sudo ufw reset
sudo ufw status
# beth@home:~$
ssh shop
# beth@shop:~$
sudo ufw default deny incoming
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx HTTP'
sudo ufw allow from 192.168.50.0/24 to any port 5000 proto tcp
sudo ufw show added
sudo ufw enable
# beth@home:~$
ssh shop
# beth@shop:~$
hostname
# guest@phone:~$
curl -sS -m 10 -o /dev/null -w '%{http_code}\n' shop
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
