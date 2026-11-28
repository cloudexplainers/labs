# Tailscale: Full Tutorial for Beginners

Video: https://youtu.be/0zmnRT455Xc  
Written version: https://cloudexplainers.com/tailscale-full-tutorial-for-beginners/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/booking/app.py`](lab/booking/app.py)
- [`lab/booking/booking.service`](lab/booking/booking.service)
- [`lab/doorcam/app.py`](lab/doorcam/app.py)
- [`lab/doorcam/doorcam.service`](lab/doorcam/doorcam.service)
- [`lab/headscale/config.yaml`](lab/headscale/config.yaml)
- [`lab/whoami/app.py`](lab/whoami/app.py)
- [`lab/whoami/whoami.service`](lab/whoami/whoami.service)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### Locked out from the cafe

```sh
# john@laptop:~$
curl -sS -m 5 http://192.168.50.10:8080
curl -s http://basement:8080
tailscale status
```

### Install on Linux

```sh
# john@basement:~$
curl -fsSL https://tailscale.com/install.sh | sh
tailscale version
systemctl status tailscaled --no-pager
tailscale status
```

### Log in

```sh
# john@headscale:~$
sudo headscale users create john
sudo headscale users list
# john@basement:~$
sudo tailscale up --login-server https://headscale.lab
# john@headscale:~$
sudo headscale auth register --auth-id hskey-authreq-AmvwO2H7_ZkJ5oV3RsdlA89- --user john
# john@basement:~$
tailscale ip -4
ip -br addr show tailscale0
ip -br -4 addr show eth0
```

### A second device

```sh
# john@laptop:~$
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up --login-server https://headscale.lab
# john@headscale:~$
sudo headscale auth register --auth-id hskey-authreq--t3WTU0Vep8cVa1knYtMqu6M --user john
# john@laptop:~$
tailscale status
ping -c 3 100.64.0.1
curl -s http://100.64.0.1:8080
```

### Names with MagicDNS

```sh
# john@laptop:~$
curl -s http://basement:8080
cat /etc/resolv.conf
getent hosts basement
```

### Direct or relayed

```sh
# john@laptop:~$
tailscale ping -c 10 basement
tailscale netcheck
# root@building-router:~#
conntrack -L -p udp 2>/dev/null | grep 'dport=41641'
```

### Adding a second person

```sh
# john@headscale:~$
sudo headscale users create jen
sudo headscale users list
sudo headscale preauthkeys create --user 2 --expiration 1h
sudo tailscale up --login-server https://headscale.lab --auth-key hskey-auth-PawaGVb…
# jen@jen-laptop:~$
curl -s http://basement:8080
tailscale ping -c 8 basement
tailscale status
# john@basement:~$
tailscale whois 100.64.0.3
```

### Access rules

```sh
# jen@jen-laptop:~$
nc -zv -w 3 basement 22
ping -c 2 laptop
# john@headscale:~$
cat policy.hujson
sudo headscale policy set -f policy.hujson
# jen@jen-laptop:~$
curl -s http://basement:8080
nc -zv -w 3 basement 22
ping -c 2 -W 2 laptop
# john@laptop:~$
nc -zv -w 3 basement 22
```

### Tailscale SSH and files

```sh
# john@headscale:~$
cat policy.hujson
sudo headscale policy set -f policy.hujson
# john@basement:~$
sudo tailscale set --ssh
# john@laptop:~$
tailscale ssh john@basement 'hostname; whoami'
# jen@jen-laptop:~$
timeout 15 tailscale ssh john@basement hostname
# john@laptop:~$
echo 'Washer 2 is out of order until Monday.' > notice.txt && cat notice.txt
sudo tailscale file cp notice.txt basement:
# john@basement:~$
sudo tailscale file get .
cat notice.txt
```

### Subnet routers

```sh
# john@laptop:~$
curl -sS -m 5 http://192.168.50.20
# john@basement:~$
echo 'net.ipv4.ip_forward = 1' | sudo tee /etc/sysctl.d/99-tailscale.conf && sudo sysctl -p /etc/sysctl.d/99-tailscale.conf
sudo tailscale set --advertise-routes=192.168.50.0/24
# john@headscale:~$
sudo headscale nodes list-routes
sudo headscale nodes approve-routes --identifier 1 --routes 192.168.50.0/24
# john@laptop:~$
curl -sS -m 5 http://192.168.50.20
sudo tailscale set --accept-routes
curl -s -m 5 http://192.168.50.20
```

### Exit nodes

```sh
# john@laptop:~$
curl -s http://whatismyip.lab
# john@basement:~$
sudo tailscale set --advertise-exit-node
# john@headscale:~$
sudo headscale nodes list-routes
sudo headscale nodes approve-routes --identifier 1 --routes 192.168.50.0/24,0.0.0.0/0,::/0
# john@laptop:~$
tailscale exit-node list
sudo tailscale set --exit-node=basement
curl -s http://whatismyip.lab
tailscale status
sudo tailscale set --exit-node=
curl -s http://whatismyip.lab
```

### Day to day

```sh
# john@laptop:~$
sudo tailscale down
curl -sS -m 5 http://basement:8080
sudo tailscale up
curl -s http://basement:8080
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
