# Linux Nginx Reverse Proxy: Full Tutorial for Beginners

Video: https://youtu.be/xbhvLOVQHlY  
Written version: https://cloudexplainers.com/linux-nginx-reverse-proxy-full-tutorial-for-beginners/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/capture.py`](lab/capture.py)
- [`lab/kiln/app.py`](lab/kiln/app.py)
- [`lab/shop/app.py`](lab/shop/app.py)
- [`lab/static/studio.css`](lab/static/studio.css)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### Inspecting Ports and Nginx

```sh
sudo ss -tlnp | grep -E 'nginx|gunicorn'
```

### Your First Reverse Proxy

```sh
cat /etc/nginx/sites-available/studio.conf
sudo ln -sf /etc/nginx/sites-available/studio.conf /etc/nginx/sites-enabled/studio.conf && sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx
curl -sI http://127.0.0.1/ | head -n 5
curl -sI http://127.0.0.1/kiln/ | head -n 5
sudo nginx -t && sudo systemctl reload nginx
curl -sI http://127.0.0.1/kiln/ | head -n 5
```

### Virtual Hosts and Static Files

```sh
grep -E 'server_name|alias|proxy_pass' /etc/nginx/sites-available/studio.conf
curl -s -H "Host: kiln.pottery.test" http://127.0.0.1/ | grep -o "<title>.*</title>"
curl -sI http://127.0.0.1/static/studio.css | head -n 6
```

### The Localhost IP Trap

```sh
curl -s http://127.0.0.1/whoami
cat /etc/nginx/proxy_params
curl -s -H "Host: shop.pottery.test" http://127.0.0.1/whoami
```

### Load Balancing with Upstream

```sh
head -n 6 /etc/nginx/sites-available/studio.conf
for i in 1 2 3 4; do curl -s http://127.0.0.1/worker; done
sudo systemctl stop studio-shop-2
for i in 1 2 3; do curl -s http://127.0.0.1/worker; done
```

### HTTPS and Redirects

```sh
sed -n '5,17p' /etc/nginx/sites-available/studio.conf
curl -sI http://127.0.0.1/ | head -n 5
curl -skI https://127.0.0.1/ | head -n 5
```

### Limits, Timeouts, and Checklist

```sh
dd if=/dev/zero bs=1M count=2 status=none | curl -sk -o /dev/null -w "HTTP %{http_code}\n" --data-binary @- https://127.0.0.1/upload
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
