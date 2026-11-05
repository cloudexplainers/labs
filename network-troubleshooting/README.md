# Every Network Troubleshooting Command You Need

Video: https://youtu.be/8jJV3esAedU  
Written version: https://cloudexplainers.com/every-network-troubleshooting-command-you-need/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Commands, in the order the video runs them

### Is the network card up?

```sh
# ana@laptop:~$
ip -brief address
curl -sS -m 5 shop.example
ip -brief address
```

### Is there a way out?

```sh
# ana@laptop:~$
ip route
curl -sS -m 5 shop.example
ip route
ping -c 2 198.51.100.10
```

### Can I reach it?

```sh
# ana@laptop:~$
ping -c 3 192.168.1.1
ping -c 3 198.51.100.10
curl -sS -m 5 shop.example
ping -c 3 198.51.100.10
```

### Where does the path stop?

```sh
# ana@laptop:~$
traceroute -n 198.51.100.10
traceroute -n -m 5 198.51.100.10
```

### Does the name work?

```sh
# ana@laptop:~$
dig +short shop.example
curl -sS -m 5 shop.example
ping -c 2 198.51.100.10
dig shop.example
```

### Is the door open?

```sh
# ana@laptop:~$
nc -zv shop.example 80
curl -sS -m 5 shop.example
ping -c 2 shop.example
nc -zv shop.example 80
```

### Who is listening?

```sh
# root@shop-server:~#
ss -tlnp
curl -s localhost
ss -tlnp
# ana@laptop:~$
nc -zv shop.example 80
```

### What does the website say?

```sh
# ana@laptop:~$
curl -I shop.example/sale
curl -I shop.example/sales.html
curl -v shop.example/sales.html
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
