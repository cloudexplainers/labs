# Why the Internet Ran Out of IP Addresses

Video: https://youtu.be/fiEesQ8xcsE  
Written version: https://cloudexplainers.com/why-the-internet-ran-out-of-ip-addresses/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/bits.py`](lab/bits.py)
- [`lab/blocks.py`](lab/blocks.py)
- [`lab/ipv4-address-space.csv`](lab/ipv4-address-space.csv)
- [`lab/web.py`](lab/web.py)

## Commands, in the order the video runs them

### An address is a number

```sh
# ana@ana-laptop:~$
python3 bits.py 192.168.1.20
python3 -c 'print(2**32)'
```

### Where the addresses went

```sh
# ana@ana-laptop:~$
python3 blocks.py ipv4-address-space.csv
grep -E '^0(17|19)/8' ipv4-address-space.csv | cut -d, -f1-3
```

### Trick one: share an address

```sh
# ana@ana-laptop:~$
ip -4 -brief address show eth0
# ben@ben-laptop:~$
ip -4 -brief address show eth0
# root@ana-router:~#
ip -4 -brief address show wan
# root@server:~#
python3 web.py 80 Hello from the server
# ana@ana-laptop:~$
curl -4 -s -m 10 server.example
# ben@ben-laptop:~$
curl -4 -s -m 10 server.example
```

### What sharing costs

```sh
# ana@ana-laptop:~$
python3 web.py 8000 "Photos from Ana's laptop"
# root@server:~#
curl -4 -sS -m 5 http://203.0.113.7:8000
```

### The real fix: IPv6

```sh
# ana@ana-laptop:~$
python3 bits.py 2001:db8:a::20
python3 -c 'print(2**128)'
hostname -I
curl -6 -s -m 10 server.example
curl -4 -s -m 10 server.example
# root@server:~#
python3 web.py 80 Hello from the server
curl -6 -s -m 5 'http://[2001:db8:a::20]:8000'
# ana@ana-laptop:~$
python3 web.py 8000 "Photos from Ana's laptop"
```

### Why the switch is slow

```sh
# ben@ben-laptop:~$
hostname -I
curl -6 -sS -m 5 server.example
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
