# How to Fix Cloudflare Tunnel Errors in a Homelab

Video: https://youtu.be/gg3jIZ_6xQ0  
Written version: https://cloudexplainers.com/how-to-fix-cloudflare-tunnel-errors-in-a-homelab/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/club/nas/serve.py`](lab/club/nas/serve.py)
- [`lab/club/nas/www/index.html`](lab/club/nas/www/index.html)
- [`lab/club/site/index.html`](lab/club/site/index.html)
- [`lab/friend/Dockerfile`](lab/friend/Dockerfile)
- [`lab/named/config-1.yml`](lab/named/config-1.yml)
- [`lab/named/config-2.yml`](lab/named/config-2.yml)
- [`lab/server/Dockerfile`](lab/server/Dockerfile)
- [`lab/steps/1/compose.yaml`](lab/steps/1/compose.yaml)
- [`lab/steps/2/compose.yaml`](lab/steps/2/compose.yaml)
- [`lab/steps/3/compose.yaml`](lab/steps/3/compose.yaml)
- [`lab/steps/4/compose.yaml`](lab/steps/4/compose.yaml)
- [`lab/steps/5/compose.yaml`](lab/steps/5/compose.yaml)
- [`lab/steps/6/compose.yaml`](lab/steps/6/compose.yaml)

## Commands, in the order the video runs them

### Fine at home, 502 outside

```sh
# ana@club-server:~/club$
curl -s -o /dev/null -w '%{http_code}\n' localhost:8080
# ben@laptop:~$
curl -sI https://moments-yourself-led-relevance.trycloudflare.com | head -1
```

### Read the tunnel's log

```sh
# ana@club-server:~/club$
docker compose logs tunnel | grep -o 'error="[^"]*"' | tail -1
```

### The fix: the service's name

```sh
# ana@club-server:~/club$
docker compose up -d
docker compose logs tunnel | grep -o 'https://[a-z-]*.trycloudflare.com' | tail -1
# ben@laptop:~$
curl -sI https://grab-election-representatives-participation.trycloudflare.com | head -1
```

### When the app is down

```sh
# ana@club-server:~/club$
docker compose stop site
# ben@laptop:~$
curl -sI https://grab-election-representatives-participation.trycloudflare.com | head -1
# ana@club-server:~/club$
docker compose logs tunnel | grep -o 'error="[^"]*"' | tail -1
```

### Error 1033: no tunnel connected

```sh
# ana@club-server:~/club$
sudo systemctl restart docker
docker compose ps -a --format 'table {{.Service}}\t{{.Status}}'
# ben@laptop:~$
curl -sI https://grab-election-representatives-participation.trycloudflare.com | head -1
# ana@club-server:~/club$
grep -n restart compose.yaml
docker compose up -d
sudo systemctl restart docker
docker compose ps -a --format 'table {{.Service}}\t{{.Status}}'
docker compose logs tunnel | grep -o 'https://[a-z-]*.trycloudflare.com' | tail -1
```

### Running, and still 1033

```sh
# ana@club-server:~/club$
sudo iptables -I DOCKER-USER -p udp --dport 7844 -j DROP
docker compose up -d --force-recreate tunnel
docker compose ps --format 'table {{.Service}}\t{{.Status}}'
# ben@laptop:~$
curl -sI https://intranet-hope-bias-recognised.trycloudflare.com | head -1
# ana@club-server:~/club$
docker compose logs --no-log-prefix tunnel | grep -E '[|]  (UDP|SUMMARY)' | cut -c 26-
docker compose logs tunnel | grep -o 'error="[^"]*"' | tail -1
docker compose logs --no-log-prefix tunnel | grep -E 'Switching|Registered' | sed -E 's/^.{11}//; s/ (connIndex|connection|event|ip|location)=[^ ]+//g'
grep -n protocol compose.yaml
docker compose up -d
docker compose logs --no-log-prefix tunnel | grep -E 'Initial protocol|Registered' | sed -E 's/^.{11}//; s/ (connIndex|connection|event|ip|location)=[^ ]+//g'
```

### A NAS on HTTPS

```sh
# ana@club-server:~/club$
docker compose up -d
# ben@laptop:~$
curl -sI https://mlb-site-peers-predict.trycloudflare.com | head -1
# ana@club-server:~/club$
docker compose logs nas-tunnel | grep -o 'error="[^"]*"' | tail -1
grep -n tls compose.yaml
docker compose up -d
# ben@laptop:~$
curl -sI https://aus-release-set-sizes.trycloudflare.com | head -1
```

### A named tunnel's rules

```sh
# ana@club-server:~$
cat .cloudflared/config.yml
cloudflared tunnel ingress validate
tail -1 .cloudflared/config.yml
cloudflared tunnel ingress validate
cloudflared tunnel ingress rule https://game.example.com
cloudflared tunnel ingress rule https://games.example.com
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
