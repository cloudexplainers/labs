# How to Fix No Space Left on Device in Linux

Video: https://youtu.be/grTIx6emfrQ  
Written version: https://cloudexplainers.com/how-to-fix-no-space-left-on-device-in-linux/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/fill_log.py`](lab/fill_log.py)
- [`lab/fill_sessions.py`](lab/fill_sessions.py)
- [`lab/logrotate-shop`](lab/logrotate-shop)
- [`lab/shop.py`](lab/shop.py)
- [`lab/shop.service`](lab/shop.service)

## Commands, in the order the video runs them

### Nothing will save

```sh
# ana@shop:~$
curl -s -d tea=sencha localhost:8080/order
echo "order more sencha" > todo.txt
```

### Step 1: which disk

```sh
# ana@shop:~$
df -h
```

### Step 2: what fills it

```sh
# ana@shop:~$
sudo du -xh -d1 / | sort -h | tail -n 4
sudo du -xh -d1 /var | sort -h | tail -n 4
sudo find / -xdev -type f -size +100M -exec ls -lh {} +
sudo tail -n 3 /var/log/shop/access.log
```

### The deleted log

```sh
# ana@shop:~$
sudo rm /var/log/shop/access.log
df -h /
sudo lsof +L1
sudo systemctl restart shop
df -h /
curl -s -d tea=sencha localhost:8080/order
sudo du -sh /var/cache/apt /var/log/journal
sudo apt clean
df -h /
```

### Space left, still full

```sh
# ana@shop:~$
curl -s -d tea=matcha localhost:8080/order
df -h /
df -i /
sudo du --inodes -xd1 /var/lib/shop | sort -n
sudo find /var/lib/shop/sessions -type f -mtime +7 | wc -l
sudo find /var/lib/shop/sessions -type f -mtime +7 -delete
df -i /
curl -s -d tea=matcha localhost:8080/order
```

### Stop it coming back

```sh
# ana@shop:~$
cat /etc/logrotate.d/shop
sudo logrotate -f /etc/logrotate.d/shop
ls -lh /var/log/shop
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
