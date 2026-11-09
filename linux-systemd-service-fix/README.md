# How to Fix a Linux systemd Service That Won't Start

Video: https://youtu.be/uDZlfKJ8FMk  
Written version: https://cloudexplainers.com/how-to-fix-a-linux-systemd-service-that-won-t-start/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile.server`](lab/Dockerfile.server)
- [`lab/teashop.service`](lab/teashop.service)
- [`lab/teashop/app.py`](lab/teashop/app.py)
- [`lab/teashop/stock.txt`](lab/teashop/stock.txt)
- [`lab/teashop2.service`](lab/teashop2.service)
- [`lab/v2/app.py`](lab/v2/app.py)

## Commands, in the order the video runs them

### Started, but not running

```sh
# ana@shop:~$
sudo systemctl start teashop
curl -sS localhost:8080
systemctl is-active teashop
```

### The usual fix: read the reason

```sh
# ana@shop:~$
systemctl status teashop --no-pager -n 0
grep -n ExecStart /etc/systemd/system/teashop.service
ls /usr/bin/python*
sudo sed -i 's|/usr/bin/python |/usr/bin/python3 |' /etc/systemd/system/teashop.service
grep -n ExecStart /etc/systemd/system/teashop.service
sudo systemctl restart teashop
systemctl status teashop --no-pager -n 0
sudo systemctl daemon-reload
sudo systemctl restart teashop
systemctl status teashop --no-pager -n 0
curl -s localhost:8080
```

### Works by hand, fails as a service

```sh
# ana@shop:~$
cd teashop
# ana@shop:~/teashop$
grep -n TEA_STOCK app.py
echo $TEA_STOCK
sudo systemctl stop teashop
nohup python3 app.py > test.log 2>&1 &
curl -s localhost:8080
sudo systemctl restart teashop
sudo systemctl status teashop --no-pager
sudo journalctl -u teashop --no-pager -n 14 -o cat
sudo sed -i '/^WorkingDirectory=/a Environment=TEA_STOCK=/home/ana/teashop/stock.txt' /etc/systemd/system/teashop.service
cat /etc/systemd/system/teashop.service
sudo systemctl daemon-reload
sudo systemctl restart teashop
systemctl is-active teashop
```

### The port is already taken

```sh
# ana@shop:~/teashop$
sudo journalctl -u teashop --no-pager -n 9 -o cat
sudo ss -ltnp 'sport = :8080'
ps -o pid,user,etime,args -p 224
```

### Start request repeated too quickly

```sh
# ana@shop:~/teashop$
kill 224
sudo systemctl start teashop
sudo journalctl -u teashop --no-pager -n 3 -o cat
systemctl show teashop -p StartLimitBurst -p StartLimitIntervalUSec
sudo systemctl reset-failed teashop
sudo systemctl start teashop
systemctl status teashop --no-pager -n 0
curl -s localhost:8080
```

### Catch it before you start

```sh
# ana@shop:~/teashop$
cd ~/drafts
# ana@shop:~/drafts$
systemd-analyze verify teashop.service
systemd-analyze verify teashop2.service
systemd-analyze verify /etc/systemd/system/teashop.service && echo no problems found
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
