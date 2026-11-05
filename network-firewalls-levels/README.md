# The 5 Levels of Network Firewalls

Video: https://youtu.be/lsshTgHQP9A  
Written version: https://cloudexplainers.com/the-5-levels-of-network-firewalls/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Commands, in the order the video runs them

### Ana's open database

```sh
# ana@stranger:~$
nmap -Pn -p 22,80,5432 web db | grep -E 'report|/tcp'
nc -zv -w 3 db 5432
```

### Level 1: Packet filter

```sh
# ana@db:~$
cat firewall.nft
sudo nft -f firewall.nft
# ana@stranger:~$
nc -zv -w 3 db 5432
# ana@web:~$
nc -zv -w 3 db 5432
# ana@stranger:~$
nmap -Pn -p 22,5432 db | grep /tcp
# ana@db:~$
curl -m 5 http://updates.example/
```

### Level 2: Stateful firewall

```sh
# ana@db:~$
sudo nft insert rule inet fw input ct state established,related accept
curl -m 5 http://updates.example/
sudo nft list chain inet fw input
sudo conntrack -L -p tcp --dport 80 2>/dev/null | awk '{print $4, $5, $6, $7, $8}'
# ana@stranger:~$
nc -zv -w 3 db 5432
```

### Level 3: Network firewall

```sh
# ana@stranger:~$
nc -zv -w 3 web 22
# ana@shop-router:~$
cat edge.nft
sudo nft -f edge.nft
# ana@stranger:~$
curl -s http://shop.example/
nc -zv -w 3 web 22
nc -zv -w 3 db 22
# ana@ana-home:~$
nc -zv -w 3 web 22
# ana@db:~$
curl -m 5 http://updates.example/
# ana@shop-router:~$
sudo nft list chain inet edge forward | grep counter
```

### Level 5: Application firewall

```sh
# ana@stranger:~$
curl -s http://shop.example/admin
# ana@proxy:~$
cat shop-proxy.conf
sudo cp shop-proxy.conf /etc/nginx/conf.d/ && sudo nginx
# ana@shop-router:~$
cat edge-proxy.nft | grep 'tcp dport 80'
sudo nft -f edge-proxy.nft
# ana@stranger:~$
getent hosts shop.example
curl -s http://shop.example/products
curl -s -o /dev/null -w '%{http_code}\n' http://shop.example/admin
curl -m 5 http://198.51.100.10/admin
for i in $(seq 20); do curl -s -o /dev/null -w '%{http_code}\n' http://shop.example/; done | sort | uniq -c
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
