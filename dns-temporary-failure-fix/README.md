# How to Fix DNS 'Temporary Failure in Name Resolution' on Linux

Video: https://youtu.be/_i9eT5e7uxA  
Written version: https://cloudexplainers.com/how-to-fix-dns-temporary-failure-in-name-resolution-on-linux/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/pc/50-depot.yaml`](lab/pc/50-depot.yaml)
- [`lab/pc/resolv-link.service`](lab/pc/resolv-link.service)
- [`lab/router/depot.conf`](lab/router/depot.conf)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### A number answers, a name doesn't

```sh
# ana@dispatch:~$
ping -c 1 archive.ubuntu.com
ping -c 2 1.1.1.1
```

### The fix everyone posts

```sh
# ana@dispatch:~$
cat /etc/resolv.conf
echo 'nameserver 1.1.1.1' | sudo tee /etc/resolv.conf
ping -c 1 archive.ubuntu.com
sudo systemctl restart systemd-resolved
ping -c 1 archive.ubuntu.com
grep nameserver /etc/resolv.conf
ls -l /etc/resolv.conf
```

### Who is it asking?

```sh
# ana@dispatch:~$
ping -c 1 archive.ubunto.com
resolvectl status eth0
resolvectl query archive.ubuntu.com
sudo cat /etc/netplan/50-depot.yaml
sudo netplan apply
resolvectl status eth0
ping -c 1 archive.ubuntu.com
sudo apt-get update
ping -c 1 archive.ubunto.com
```

### Nobody at 127.0.0.53

```sh
# ana@dispatch:~$
ping -c 1 archive.ubuntu.com
dig archive.ubuntu.com
systemctl status systemd-resolved
sudo systemctl enable --now systemd-resolved
ping -c 1 archive.ubuntu.com
sudo true
grep 127.0.1.1 /etc/hosts
sudo sed -i 's/courier-pc/dispatch/' /etc/hosts
sudo systemctl start systemd-resolved
```

### When outgoing DNS is blocked

```sh
# ana@dispatch:~$
time ping -c 1 debian.org
dig @192.168.73.1 debian.org
curl -sS -o /dev/null -w '%{http_code}\n' https://1.1.1.1
sudo ufw status verbose
sudo ufw allow out 53
curl -sS -o /dev/null -w '%{http_code}\n' https://debian.org
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
