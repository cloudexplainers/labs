# Never Ignore a Security Update

Video: https://youtu.be/JUCR77a7xTI  
Written version: https://cloudexplainers.com/never-ignore-a-security-update/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/short.tpl`](lab/short.tpl)
- [`lab/trivy.yaml`](lab/trivy.yaml)

## Commands, in the order the video runs them

### The message it's easy to skip

```sh
# ana@laptop:~$
ssh shop
```

### What is inside an update

```sh
# ana@shop:~$
apt list --upgradable 2>/dev/null | grep -E '^(sudo|openssh-server|openssl)/'
ssh -V
apt changelog openssh-server 2>/dev/null | grep -m1 -B2 -A4 'signal handler'
```

### Scanning Ana's server

```sh
# ana@shop:~$
trivy rootfs --ignore-unfixed / | grep Total
trivy rootfs --ignore-unfixed -s HIGH,CRITICAL -f template -t @short.tpl /
```

### Why waiting is risky

```sh
# ana@shop:~$
cat /etc/apt/apt.conf.d/20auto-upgrades
```

### Installing the updates

```sh
# ana@shop:~$
sudo apt update
sudo apt upgrade -y
```

### Restarts finish the job

```sh
# ana@shop:~$
trivy rootfs --ignore-unfixed /
ssh -V
```

### Updates that install themselves

```sh
# ana@shop:~$
sudo sed -i 's/"0"/"1"/' /etc/apt/apt.conf.d/20auto-upgrades
cat /etc/apt/apt.conf.d/20auto-upgrades
sudo unattended-upgrade --dry-run --debug 2>&1 | grep -m1 'Allowed origins'
systemctl status apt-daily-upgrade.timer | grep -E 'Active|Trigger:'
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
