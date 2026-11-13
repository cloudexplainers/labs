# How to Fix Linux apt 'Could Not Get Lock' Errors (Ubuntu)

Video: https://youtu.be/7q3QUgTMhWo  
Written version: https://cloudexplainers.com/how-to-fix-linux-apt-could-not-get-lock-errors-ubuntu/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### Could not get lock

```sh
# ana@catalog:~$
sudo apt-get install -y htop
```

### The quick fix: read it, then wait

```sh
# ana@catalog:~$
ps -o pid,etime,cmd -p 471
systemctl is-active apt-daily-upgrade.service
sudo apt install -y htop
```

### Who holds it on a fresh server

```sh
# ana@catalog:~$
systemctl cat apt-daily-upgrade.timer
sudo tail -n 3 /var/log/unattended-upgrades/unattended-upgrades.log | cut -c 12-95
systemctl is-active apt-daily-upgrade.service
```

### Who holds it: another terminal

```sh
# ana@catalog:~$
sudo apt-get install -y tree
ps -o pid,tty,etime,cmd -p 1454
ps -o ruser,etime,cmd -C sudo
sudo lsof /var/lib/dpkg/lock-frontend
# ben@catalog:~$
sudo apt install build-essential
```

### Why deleting the lock file is wrong

```sh
# ana@catalog:~$
ls -l /var/lib/dpkg/lock*
sudo lsof /var/lib/dpkg/lock-frontend
```

### What killing the holder costs

```sh
# ana@catalog:~$
sudo apt-get install -y jq
sudo kill -9 1505
sudo apt-get install -y jq
sudo dpkg --configure -a
sudo dpkg --audit
sudo dpkg --audit
```

### In scripts: wait for the lock

```sh
# ana@catalog:~$
cat setup.sh
bash setup.sh
cat setup.sh
bash setup.sh
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
