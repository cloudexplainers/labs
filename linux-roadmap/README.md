# The Linux Roadmap for Beginners

Video: https://youtu.be/XHHgrmSQYqU  
Written version: https://cloudexplainers.com/the-linux-roadmap-for-beginners/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile.laptop`](lab/Dockerfile.laptop)
- [`lab/Dockerfile.server`](lab/Dockerfile.server)
- [`lab/check-site.sh`](lab/check-site.sh)
- [`lab/cron.txt`](lab/cron.txt)

## Commands, in the order the video runs them

### Where to start

```sh
# ana@server:~$
ls /
```

### The shell

```sh
# ana@server:~$
whoami
pwd
cd /var/log
# ana@server:/var/log$
ls
cd ~
```

### Files and text

```sh
# ana@server:~$
grep PRETTY /etc/os-release
ls /usr/bin | wc -l
echo "<h1>Ana's Tea Shop</h1>" > index.html
cat index.html
```

### Users and permissions

```sh
# ana@server:~$
id
ls -l /etc/shadow
cat /etc/shadow
apt update
sudo apt update
```

### Installing software

```sh
# ana@server:~$
sudo apt install -y nginx
nginx -v
ls /etc/nginx
```

### Processes and services

```sh
# ana@server:~$
systemctl status nginx --no-pager | head -3
ps -C nginx -o user,pid,cmd
sudo cp index.html /var/www/html/index.html
curl -s localhost
sudo pkill -9 nginx
curl -sS localhost
systemctl is-active nginx
sudo journalctl -u nginx --no-pager | tail -3
sudo mkdir -p /etc/systemd/system/nginx.service.d
printf '[Service]\nRestart=always\n' | sudo tee /etc/systemd/system/nginx.service.d/restart.conf
sudo systemctl daemon-reload
sudo systemctl start nginx
sudo pkill -9 nginx
sleep 1; systemctl is-active nginx
curl -s localhost
```

### Networking and SSH

```sh
# ana@server:~$
ip -br address show eth0
ss -tln
# ana@laptop:~$
curl -s http://server
ssh-keygen -t ed25519 -N '' -q -f ~/.ssh/id_ed25519
ssh-copy-id -o StrictHostKeyChecking=accept-new ana@server
ssh ana@server hostname
```

### Scripts and schedules

```sh
# ana@server:~$
df -h /
cat check-site.sh
./check-site.sh
cat cron.txt
crontab cron.txt
sudo pkill -9 nginx
cat site.log
sudo journalctl -u cron --no-pager | grep CMD | tail -2
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
