# How a Load Balancer Works with HAProxy

Video: https://youtu.be/kkGClEISoB0  
Written version: https://cloudexplainers.com/how-a-load-balancer-works-with-haproxy/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/signup.py`](lab/signup.py)
- [`lab/signup.service`](lab/signup.service)
- [`lab/steps/0/haproxy.cfg`](lab/steps/0/haproxy.cfg)
- [`lab/steps/1/haproxy.cfg`](lab/steps/1/haproxy.cfg)
- [`lab/steps/2/haproxy.cfg`](lab/steps/2/haproxy.cfg)
- [`lab/steps/3/haproxy.cfg`](lab/steps/3/haproxy.cfg)
- [`lab/steps/4/haproxy.cfg`](lab/steps/4/haproxy.cfg)
- [`lab/steps/5/haproxy.cfg`](lab/steps/5/haproxy.cfg)
- [`lab/ubuntu-haproxy.cfg`](lab/ubuntu-haproxy.cfg)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### One address, three servers

```sh
# ben@laptop:~$
wrk -t2 -c32 -d10s http://race.lan/
wrk -t2 -c32 -d10s http://race.lan/
```

### Ana's HAProxy config

```sh
# ana@lb:~$
sed -n '/^frontend/,/web3/p' /etc/haproxy/haproxy.cfg
sudo haproxy -c -f /etc/haproxy/haproxy.cfg
# ben@laptop:~$
for i in 1 2 3 4 5 6; do curl -s race.lan/hello; done
```

### When a server goes down

```sh
# ana@web2:~$
sudo systemctl stop signup
# ben@laptop:~$
for i in 1 2 3 4 5 6; do curl -s race.lan/hello | head -1; done
for i in 1 2 3; do curl -s -o /dev/null -w '%{http_code} after %{time_total} s\n' race.lan/hello; done
# ana@lb:~$
grep ' 503 ' /var/log/haproxy.log | tail -1
```

### Health checks

```sh
# ana@lb:~$
sudo systemctl reload haproxy
# ana@web2:~$
sudo systemctl stop signup; date +%T
# ana@lb:~$
grep 'web2 is DOWN' /var/log/haproxy.log
# ben@laptop:~$
for i in 1 2 3 4 5 6; do curl -s race.lan/hello; done
```

### Up, but broken

```sh
# ana@web3:~$
df -h /var/lib/signup
# ben@laptop:~$
for i in 1 2 3; do curl -s -d name=Ben race.lan/signup; done
# ana@lb:~$
grep -n 'httpchk' /etc/haproxy/haproxy.cfg
sudo systemctl reload haproxy
grep 'web3 is DOWN' /var/log/haproxy.log | tail -1
# ben@laptop:~$
for i in 1 2 3; do curl -s -d name=Ben race.lan/signup; done
```

### The basket that empties

```sh
# ben@laptop:~$
curl -s -c jar -b jar 'race.lan/add?race=10K'
for i in 1 2 3; do curl -s -b jar race.lan/basket; done
# ana@lb:~$
grep -n 'cookie' /etc/haproxy/haproxy.cfg
# ben@laptop:~$
curl -s -c jar -b jar 'race.lan/add?race=10K'
for i in 1 2 3; do curl -s -b jar race.lan/basket; done
grep -o 'SERVERID.*' jar
```

### Who sent this request?

```sh
# ben@laptop:~$
hostname -I
# ana@web2:~$
journalctl -u signup -o cat | grep hello | tail -1
# ana@lb:~$
grep -n 'forwardfor' /etc/haproxy/haproxy.cfg
sudo systemctl reload haproxy
# ben@laptop:~$
for i in 1 2 3; do curl -s race.lan/hello; done
# ana@web2:~$
journalctl -u signup -o cat | grep hello | tail -1
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
