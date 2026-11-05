# DNS Will Finally Make Sense After This

Video: https://youtu.be/b6w2ul6s174  
Written version: https://cloudexplainers.com/dns-will-finally-make-sense-after-this/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Commands, in the order the video runs them

### A move that half worked

```sh
# ana@ana-laptop:~$
curl -s shop.test
# ben@ben-laptop:~$
curl -s shop.test
```

### Names and addresses

```sh
# ben@ben-laptop:~$
cat /etc/resolv.conf
```

### Who has the answer

```sh
# ben@ben-laptop:~$
dig +trace shop.test
```

### DNS records

```sh
# ana@shop-dns:/etc/bind$
cat db.shop.test
# ben@ben-laptop:~$
dig +noall +answer www.shop.test shop.test MX
```

### Caching and TTL

```sh
# ben@ben-laptop:~$
dig +noall +answer +stats shop.test
# root@resolver-2:~#
unbound-control dump_cache | grep '^shop.test'
# root@root-server:~#
journalctl -u named -o cat | grep 'query: shop.test'
```

### Why Ben saw the old shop

```sh
# ana@shop-dns:/etc/bind$
grep 10.53.0.50 db.shop.test
sudo sed -i 's/10.53.0.50/10.53.0.60/' db.shop.test
sudo rndc reload shop.test
dig @10.53.0.13 +short shop.test
# ben@ben-laptop:~$
curl -s shop.test
dig +noall +answer shop.test
dig @ns.shop.test +noall +answer shop.test
for i in $(seq 7); do dig +noall +answer shop.test; sleep 30; done
```

### Moving the right way

```sh
# ben@ben-laptop:~$
curl -s shop.test
# ana@shop-dns:/etc/bind$
sudo sed -i 's/ 300 / 30 /' db.shop.test
sudo rndc reload shop.test
grep 10.53.0.50 db.shop.test
# ben@ben-laptop:~$
dig +noall +answer shop.test
dig +noall +answer shop.test
# ana@shop-dns:/etc/bind$
sudo sed -i 's/10.53.0.50/10.53.0.60/' db.shop.test && sudo rndc reload shop.test
# ben@ben-laptop:~$
for i in $(seq 5); do dig +noall +answer shop.test; sleep 10; done
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
