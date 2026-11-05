# How the Internet Works

Video: https://youtu.be/Tl9xLA366Ek  
Written version: https://cloudexplainers.com/how-the-internet-works/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Commands, in the order the video runs them

### A site nobody can find

```sh
# ana@laptop:~$
curl -m 5 http://video.example/
ping -n -c 2 video.example
# root@video:~#
vtysh -c 'configure' -c 'router bgp 64503' -c 'network 198.51.100.0/24'
# ana@laptop:~$
curl -m 5 http://video.example/
```

### BGP: telling the world

```sh
# root@carrier2:~#
vtysh -c 'show ip bgp'
# root@carrier1:~#
vtysh -c 'show ip bgp'
# root@isp:~#
vtysh -c 'show ip bgp'
```

### Picking a path

```sh
# root@isp:~#
vtysh -c 'show ip bgp 198.51.100.0/24'
# ana@laptop:~$
traceroute -n -q 1 video.example
```

### When a cable breaks

```sh
# root@isp:~#
vtysh -c 'show ip bgp neighbors 192.0.2.3' | grep -E 'Hold time is|BGP state'
# ana@laptop:~$
ping -n -i 0.2 -c 100 -q video.example
# root@isp:~#
vtysh -c 'show ip bgp'
# ana@laptop:~$
traceroute -n -q 1 video.example
```

### When a network vanishes

```sh
# root@video:~#
vtysh -c 'configure' -c 'router bgp 64503' -c 'no network 198.51.100.0/24'
# root@carrier1:~#
vtysh -c 'show ip bgp 198.51.100.0/24'
# ana@laptop:~$
curl -m 5 http://video.example/
# root@video:~#
wget -qO- http://198.51.100.10/
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
