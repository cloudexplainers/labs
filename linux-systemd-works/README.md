# How Linux systemd Works

Video: https://youtu.be/Z50E2qS6Yg0  
Written version: https://cloudexplainers.com/how-linux-systemd-works/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile.server`](lab/Dockerfile.server)
- [`lab/teashop.service`](lab/teashop.service)
- [`lab/teashop/app.py`](lab/teashop/app.py)
- [`lab/teashop/refresher.py`](lab/teashop/refresher.py)

## Commands, in the order the video runs them

### Gone after a reboot

```sh
# ana@shop:~/teashop$
nohup python3 app.py > shop.log 2>&1 &
curl -s localhost:8080
sudo reboot
# ana@shop:~$
curl -sS localhost:8080
ps -C python3
```

### Who starts everything?

```sh
# ana@shop:~$
ps -p 1 -o pid,lstart,comm
systemctl list-units --type=service --state=running --no-legend --plain
# ana@shop:~/teashop$
nohup python3 app.py > shop.log 2>&1 &
ps -o pid,ppid,args -C python3
kill 103
ps -o pid,ppid,args -C python3
```

### A unit file: the recipe

```sh
# ana@shop:~$
cat /etc/systemd/system/teashop.service
sudo systemctl daemon-reload
sudo systemctl start teashop
systemctl status teashop --no-pager
curl -s localhost:8080
```

### Started is not enabled

```sh
# ana@shop:~$
systemctl is-enabled teashop
sudo reboot
curl -sS localhost:8080
systemctl is-active teashop
sudo systemctl enable teashop
sudo reboot
curl -s localhost:8080
```

### When the app crashes

```sh
# ana@shop:~$
systemctl show teashop -p MainPID
sudo kill -9 74
systemctl show teashop -p MainPID -p NRestarts
sudo journalctl -u teashop --no-pager -n 6 -o cat
curl -s localhost:8080
```

### Stop means all of it

```sh
# ana@shop:~$
systemd-cgls -u teashop.service --no-pager
sudo systemctl stop teashop
ps -C python3
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
