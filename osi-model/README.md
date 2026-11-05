# The OSI Model Will Finally Make Sense After This

Video: https://youtu.be/BgXdG56JJbA  
Written version: https://cloudexplainers.com/the-osi-model-will-finally-make-sense-after-this/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Commands, in the order the video runs them

### Catching one request

```sh
# sam@shop-server:~$
sudo tcpdump -i eth0 -w shop.pcap tcp port 80
# ana@laptop:~$
sudo tcpdump -i eth0 -w ana.pcap tcp port 80
curl shop.example
tshark -r ana.pcap
tshark -r ana.pcap -Y http.request -V | grep -v '^ '
```

### Layer 1: Physical

```sh
# ana@laptop:~$
sudo ethtool eth0 | grep -E 'Speed|Link detected'
tshark -r ana.pcap -Y http.request -V | grep -v '^ '
```

### Layer 2: Data link

```sh
# ana@laptop:~$
ip -brief link
ip neigh
tshark -r ana.pcap -Y http.request -T fields -E header=y -e eth.src -e eth.dst | column -t
# sam@shop-server:~$
tshark -r shop.pcap -Y http.request -T fields -E header=y -e eth.src -e eth.dst | column -t
```

### Layer 3: Network

```sh
# ana@laptop:~$
tshark -r ana.pcap -Y http.request -T fields -E header=y -e ip.src -e ip.dst -e ip.ttl | column -t
# sam@shop-server:~$
tshark -r shop.pcap -Y http.request -T fields -E header=y -e ip.src -e ip.dst -e ip.ttl | column -t
```

### Layer 4: Transport

```sh
# ana@laptop:~$
tshark -r ana.pcap -Y http.request -T fields -E header=y -e tcp.srcport -e tcp.dstport | column -t
# sam@shop-server:~$
tshark -r shop.pcap -Y http.request -T fields -E header=y -e tcp.srcport -e tcp.dstport | column -t
```

### Layers 5, 6 and 7

```sh
# ana@laptop:~$
tshark -r ana.pcap -Y http.request -T fields -E header=y -e http.request.method -e http.host | column -t
# sam@shop-server:~$
tshark -r shop.pcap -Y http.request -T fields -E header=y -e http.request.method -e http.host | column -t
```

### What changed on the way

```sh
# ana@laptop:~$
tshark -r ana.pcap -Y http.request -T fields -E header=y -e frame.len -e ip.hdr_len -e tcp.hdr_len -e tcp.len | column -t
```

### Troubleshooting by layer

```sh
# ana@laptop:~$
ip -brief link show eth0
ip neigh
ping -c 2 -W 1 192.168.1.1
ping -c 2 -W 1 192.168.1.1
ping -c 2 -W 1 198.51.100.10
ping -c 2 198.51.100.10
curl -sS shop.example
curl -I shop.example/sale
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
