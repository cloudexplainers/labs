# How to Fix Network 'No Route to Host' Errors on Linux

Video: https://youtu.be/r28RihiAa4Q  
Written version: https://cloudexplainers.com/how-to-fix-network-no-route-to-host-errors-on-linux/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/files/cars.py`](lab/files/cars.py)
- [`lab/files/tracker.py`](lab/files/tracker.py)
- [`lab/files/tracker.service`](lab/files/tracker.service)
- [`lab/files/weights.py`](lab/files/weights.py)
- [`lab/files/weights.service`](lab/files/weights.service)
- [`lab/rocky/Dockerfile`](lab/rocky/Dockerfile)
- [`lab/ubuntu/Dockerfile`](lab/ubuntu/Dockerfile)

## Commands, in the order the video runs them

### No route, but ping answers

```sh
# sarah@yard-office:~$
python3 cars.py
ping -c 2 tracker
```

### A firewall that says unreachable

```sh
[sarah@tracker ~]$ sudo tcpdump -nni eth0 -c 2 'tcp port 8080 or icmp'
# sarah@yard-office:~$
nc -vz tracker 8080
[sarah@tracker ~]$ sudo firewall-cmd --list-all
[sarah@tracker ~]$ sudo firewall-cmd --add-port=8080/tcp
# sarah@yard-office:~$
python3 cars.py
```

### Gone after a reload

```sh
[sarah@tracker ~]$ sudo firewall-cmd --reload
# sarah@yard-office:~$
python3 cars.py
[sarah@tracker ~]$ sudo firewall-cmd --permanent --add-port=8080/tcp
[sarah@tracker ~]$ sudo firewall-cmd --reload
[sarah@tracker ~]$ sudo firewall-cmd --list-ports
# sarah@yard-office:~$
python3 cars.py
```

### Nobody at that address

```sh
# sarah@yard-office:~$
time nc -vz -w 10 tracker 8080
ip neigh show 192.168.70.10
ping -c 3 tracker
getent hosts tracker
sudo sed -i 's/^192.168.70.10/192.168.70.11/' /etc/hosts
python3 cars.py
```

### A machine behind the router

```sh
# sarah@yard-office:~$
curl -s http://scale/
time nc -vz -w 10 scale 80
ping -c 3 scale
```

### Not the same: network unreachable

```sh
# sarah@yard-office:~$
nc -vz scale 80
ip route
ip route get 10.20.0.5
sudo ip route add default via 192.168.70.1
ip route get 10.20.0.5
curl -s http://scale/
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
