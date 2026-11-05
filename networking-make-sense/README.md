# Networking Will Finally Make Sense After This

Video: https://youtu.be/cJp3jGulgiM  
Written version: https://cloudexplainers.com/networking-will-finally-make-sense-after-this/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Commands, in the order the video runs them

### IP addresses

```sh
# ana@laptop:~$
ip -4 -brief address
```

### The local network: MAC and ARP

```sh
# ana@laptop:~$
ip link show eth0
ip neighbour
ping -c 3 192.168.1.1
# root@home-router:~#
tcpdump -n -i lan -c 2 arp
# ana@laptop:~$
ip neighbour
```

### Routers

```sh
# ana@laptop:~$
ip route
traceroute -n 198.51.100.10
```

### DNS

```sh
# ana@laptop:~$
dig +short shop.example
# root@home-router:~#
tcpdump -n -i lan -c 2 udp port 53
```

### NAT: private and public addresses

```sh
# root@home-router:~#
tcpdump -n -i any -c 2 'tcp[tcpflags] == tcp-syn'
# root@shop-server:~#
tail -n 2 /var/log/web.log
# root@isp-router:~#
ip route
```

### Ports

```sh
# root@shop-server:~#
ss -tlnp
# ana@laptop:~$
curl -s shop.example:80
nc -w 2 shop.example 22 < /dev/null
curl shop.example:8080
```

### Packets and TCP

```sh
# ana@laptop:~$
time curl -s -o photo.jpg shop.example/photo.jpg
# root@home-router:~#
tcpdump -n -i lan -U -q 'tcp port 80 and src host 198.51.100.10' -w /tmp/photo.pcap
# ana@laptop:~$
ls -l photo.jpg
# root@home-router:~#
tcpdump -n -i lan -c 3 'tcp port 80'
```

### Lost packets: TCP vs UDP

```sh
# root@home-router:~#
tc qdisc add dev lan root netem loss 10%
tc qdisc add dev wan root netem loss 10%
# ana@laptop:~$
time curl -s -o photo.jpg shop.example/photo.jpg
# root@shop-server:~#
nstat -az TcpRetransSegs
nstat -az TcpRetransSegs
# ana@laptop:~$
sha256sum photo.jpg
# root@shop-server:~#
sha256sum /srv/shop/photo.jpg
# ana@laptop:~$
for i in $(seq 1 100); do echo "message $i" > /dev/udp/198.51.100.10/9000; done
# root@shop-server:~#
wc -l received.txt
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
