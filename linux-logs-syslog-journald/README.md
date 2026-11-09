# Linux Logs: syslog vs journald

Video: https://youtu.be/k1eQkzFRNgw  
Written version: https://cloudexplainers.com/linux-logs-syslog-vs-journald/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/10-remote.conf`](lab/10-remote.conf)
- [`lab/90-central.conf`](lab/90-central.conf)
- [`lab/Dockerfile.server`](lab/Dockerfile.server)
- [`lab/teashop.service`](lab/teashop.service)
- [`lab/teashop/app.py`](lab/teashop/app.py)

## Commands, in the order the video runs them

### One error, two logs

```sh
# ana@shop:~$
curl -s "localhost:8080/order?tea=darjeeling"
grep teashop /var/log/syslog | tail -n 2
journalctl -u teashop -n 2 --no-pager
```

### Where a log line goes

```sh
# ana@shop:~$
cat /usr/lib/systemd/journald.conf.d/syslog.conf
grep -v '^#' /etc/rsyslog.d/50-default.conf | grep .
ls /var/log
file -b /var/log/syslog
file -b /var/log/journal/*/system.journal
journalctl --disk-usage
```

### Plain text: any tool reads it

```sh
# ana@shop:~$
grep "out of stock" /var/log/syslog
grep -E '^\s+(rotate [0-9]|weekly|compress)$' /etc/logrotate.d/rsyslog
```

### The journal: lines with fields

```sh
# ana@shop:~$
journalctl -u teashop -p err --no-pager
journalctl -u teashop --since "10 min ago" -o short-iso --no-pager
journalctl -u teashop -n 1 -o verbose --no-pager
```

### Who wrote this line?

```sh
# ana@shop:~$
systemctl show teashop -p MainPID
logger -t teashop --id=169 "order 99 failed: sencha is out of stock"
grep teashop /var/log/syslog | tail -n 2
journalctl -t teashop -n 2 --no-pager
journalctl -u teashop -n 1 --no-pager
journalctl -t teashop -n 1 -o verbose --no-pager
```

### Logs that leave the machine

```sh
# ana@shop:~$
cat /etc/rsyslog.d/90-central.conf
sudo systemctl restart rsyslog
curl -s "localhost:8080/order?tea=darjeeling"
# ana@logs:~$
ls /var/log/remote
tail -n 1 /var/log/remote/shop.log
# ana@shop:~$
sudo poweroff
# ana@logs:~$
tail -n 3 /var/log/remote/shop.log
grep "out of stock" /var/log/remote/shop.log
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
