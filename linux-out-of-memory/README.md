# Why Your Linux Server Runs Out of Memory

Video: https://youtu.be/7hRTfdu0jB8  
Written version: https://cloudexplainers.com/why-your-linux-server-runs-out-of-memory/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/shop.py`](lab/shop.py)
- [`lab/shop.service`](lab/shop.service)

## Commands, in the order the video runs them

### The shop is down

```sh
# ana@ubuntu:~$
systemctl status shop -n 0
journalctl -u shop -o cat | tail -n 8
```

### Reading free

```sh
# ana@ubuntu:~$
free -h
ps -eo rss,comm --sort=-rss | head -n 6
```

### Reason 1: Too many workers

```sh
# ana@ubuntu:~$
systemctl cat shop
sudo sed -i 's/WORKERS=8/WORKERS=4/' /etc/systemd/system/shop.service
sudo systemctl daemon-reload
sudo systemctl restart shop
ps -eo rss,comm --sort=-rss | head -n 6
free -h
curl localhost:8080
```

### Cache is not the problem

```sh
# ana@ubuntu:~$
tar -cf backup.tar /var/lib/shop/photos 2>/dev/null; ls -lh backup.tar
free -h
```

### Reason 2: A memory leak

```sh
# ana@ubuntu:~$
ps -C shop-worker -o pid,rss,comm
for i in $(seq 100); do curl -s localhost:8080/product > /dev/null; done
ps -C shop-worker -o pid,rss,comm
free -h
for i in $(seq 300); do curl -s localhost:8080/product > /dev/null; done
journalctl -u shop -o cat | tail -n 6
ps -C shop-worker -o pid,rss,comm
```

### Reason 3: One big job

```sh
# ana@ubuntu:~$
curl -sS localhost:8080/report
journalctl -u shop -o cat | tail -n 6
```

### The fixes

```sh
# ana@ubuntu:~$
sudo cp shop-1.1 /usr/local/bin/shop && sudo systemctl restart shop
journalctl -u shop -o cat | tail -n 1
for i in $(seq 400); do curl -s localhost:8080/product > /dev/null; done
ps -C shop-worker -o pid,rss,comm
curl -sS localhost:8080/report
sudo systemctl set-property shop.service MemoryMax=850M
systemctl status shop | grep -E 'Active:|Memory:'
systemctl is-active postgresql shop
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
