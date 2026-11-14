# Every Networking Term a Beginner Needs in 12 Minutes

Video: https://youtu.be/LHdA_MYbnpo  
Written version: https://cloudexplainers.com/every-networking-term-a-beginner-needs-in-12-minutes/

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

### One page, seventeen packets

```sh
# ana@front-desk:~$
curl http://maplevets.test
sudo tcpdump -n -t -i eth0
```

### IP address

```sh
# ana@front-desk:~$
ip -4 addr show eth0
```

### Subnet and mask

```sh
# ana@front-desk:~$
ping -c 3 printer
```

### MAC address and ARP

```sh
# ana@front-desk:~$
ip link show eth0
ip neigh
```

### Router and gateway

```sh
# ana@front-desk:~$
ip route
```

### DHCP

```sh
# ana@front-desk:~$
sudo dhclient -v -r eth0
ip -4 addr show eth0
sudo dhclient -v eth0
```

### DNS

```sh
# ana@front-desk:~$
dig maplevets.test
dig maplevets.test
```

### Ports

```sh
# ben@web:~$
ss -tln
# ana@front-desk:~$
nc -zv maplevets.test 81
nc -zv printer 9100
```

### Firewall

```sh
# ana@front-desk:~$
curl -m 10 http://maplevets.test:8080
# ben@web:~$
sudo nft list table inet filter
```

### NAT and public addresses

```sh
# ben@web:~$
tail -n 1 /var/log/web.log
# ben@clinic-router:~$
ip -4 -br addr
sudo iptables -t nat -L POSTROUTING -n -v
```

### Latency, hops and bandwidth

```sh
# ana@front-desk:~$
ping -c 3 maplevets.test
tracepath -n maplevets.test
curl -s -o x-rays.zip -w '%{size_download} bytes in %{time_total} s\n' http://maplevets.test/x-rays.zip
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
