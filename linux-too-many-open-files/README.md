# How to Fix Linux 'Too Many Open Files' Errors

Video: https://youtu.be/dO2yy0j0a9s  
Written version: https://cloudexplainers.com/how-to-fix-linux-too-many-open-files-errors/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/files/pay.sh`](lab/files/pay.sh)
- [`lab/files/washpay.py`](lab/files/washpay.py)
- [`lab/files/washpay.service`](lab/files/washpay.service)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### Payment 1,020 fails

```sh
# jim@laundromat:~$
./pay.sh 1100
journalctl -u washpay -n 2 --no-pager -o cat
```

### Count what the server holds

```sh
# jim@laundromat:~$
PID=$(systemctl show -p MainPID --value washpay)
sudo ls /proc/$PID/fd | wc -l
grep 'open files' /proc/$PID/limits
sudo lsof -p $PID | awk '{print $NF}' | sort | uniq -c | sort -rn | head -4
```

### The usual fix: raise the limit

```sh
# jim@laundromat:~$
echo '* soft nofile 8192' | sudo tee -a /etc/security/limits.conf
sudo -iu jim ulimit -n
sudo systemctl restart washpay
PID=$(systemctl show -p MainPID --value washpay)
grep 'open files' /proc/$PID/limits
```

### The service's own limit

```sh
# jim@laundromat:~$
systemctl show -p LimitNOFILESoft -p LimitNOFILE washpay
printf '[Service]\nLimitNOFILE=8192\n' | sudo tee /etc/systemd/system/washpay.service.d/nofile.conf
sudo systemctl daemon-reload && sudo systemctl restart washpay
grep 'open files' /proc/$PID/limits
systemctl show -p LimitNOFILESoft -p LimitNOFILE washpay
./pay.sh 3000
sudo ls /proc/$PID/fd | wc -l
```

### The real fix: close what you open

```sh
# jim@laundromat:~$
sudo systemctl restart washpay
PID=$(systemctl show -p MainPID --value washpay)
./pay.sh 3000
sudo ls /proc/$PID/fd | wc -l
sudo lsof -p $PID | grep -c 'washpay/washer-'
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
