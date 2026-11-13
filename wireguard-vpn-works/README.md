# How a WireGuard VPN Network Works

Video: https://youtu.be/xkpU64w1QEk  
Written version: https://cloudexplainers.com/how-a-wireguard-vpn-network-works/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/files/prices.txt`](lab/files/prices.txt)
- [`lab/site/hours.txt`](lab/site/hours.txt)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### Eight lines

```sh
# ana@laptop:~$
sudo cat /etc/wireguard/wg0.conf
```

### An address the internet can't reach

```sh
# ana@laptop:~$
curl http://203.0.113.10/hours.txt
curl -m 5 http://10.20.0.10/prices.txt
```

### Keys, not passwords

```sh
# ana@laptop:~$
umask 077
wg genkey > private.key
wg pubkey < private.key | tee public.key
ls -l
```

### The config, line by line

```sh
# ana@gateway:~$
sudo cat /etc/wireguard/wg0.conf
# ana@laptop:~$
sudo wg-quick up wg0
curl http://10.20.0.10/prices.txt
```

### What the hotel's Wi-Fi sees

```sh
# root@hotel-wifi:~#
tcpdump -ni eth0 -t -q -A -c 10 host 192.168.50.20 and not arp
tcpdump -ni eth0 -t -q -A -c 10 host 192.168.50.20 and not arp
tcpdump -ni eth0 -c 2 'udp[8] = 1'
# ana@laptop:~$
ping -c 260 -i 1 -q 10.20.0.10
```

### A door that doesn't answer

```sh
# sam@stranger:~$
for i in 1 2 3 4 5; do echo knock | nc -u -w1 203.0.113.10 51820; done
# ana@gateway:~$
sudo timeout 8 tcpdump -ni eth0 host 203.0.113.66 and not arp
# sam@stranger:~$
sudo cat /etc/wireguard/wg0.conf
ping -c 3 -W 1 10.20.0.10
sudo wg show
```

### AllowedIPs does two jobs

```sh
# ana@laptop:~$
ip route get 10.20.0.10
ip route get 203.0.113.10
ping -c 1 -I wg0 10.30.0.5
sudo ip address add 10.8.0.99/24 dev wg0
ping -c 2 -W 1 -I 10.8.0.99 10.20.0.10
ping -c 2 10.20.0.10
```

### Leaving the hotel

```sh
# ana@laptop:~$
ping -c 30 -i 0.5 10.20.0.10
# ana@gateway:~$
sudo wg show wg0 endpoints
sudo wg show wg0 endpoints
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
