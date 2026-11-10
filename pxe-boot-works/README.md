# How PXE Network Boot Works

Video: https://youtu.be/BcKKoGsCpPQ  
Written version: https://cloudexplainers.com/how-pxe-network-boot-works/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile.server`](lab/Dockerfile.server)
- [`lab/default-http`](lab/default-http)
- [`lab/nginx-site`](lab/nginx-site)
- [`lab/pxe-http.conf`](lab/pxe-http.conf)
- [`lab/pxe-uefi.conf`](lab/pxe-uefi.conf)
- [`lab/pxe.conf`](lab/pxe.conf)
- [`lab/rootfs/init`](lab/rootfs/init)
- [`lab/teacher.cfg`](lab/teacher.cfg)
- [`lab/tftp/grub/grub.cfg`](lab/tftp/grub/grub.cfg)
- [`lab/tftp/pxelinux.cfg/default`](lab/tftp/pxelinux.cfg/default)

## Commands, in the order the video runs them

### A PC with no disk

```sh
# root@lab-pc-07:~#
cat /proc/partitions
```

### Step 1: an address and a slip

```sh
# ana@pxe-server:~$
cat /etc/dnsmasq.d/pxe.conf
sudo systemctl start dnsmasq
systemctl is-active dnsmasq
```

### Step 3: find the instructions

```sh
# ana@pxe-server:~$
ls -l /srv/tftp
sudo journalctl -u dnsmasq -o cat --since 23:30:55 | grep -E 'sent /|not found'
cat /srv/tftp/pxelinux.cfg/01-52-54-00-00-00-07
sudo journalctl -u dnsmasq -o cat --since 23:31:11 | grep -E 'sent /|not found'
```

### Step 4: Linux, into memory

```sh
# ana@pxe-server:~$
cat /srv/tftp/pxelinux.cfg/default
# root@lab-pc-07:~#
cat /proc/cmdline
ls /
```

### When the file never arrives

```sh
# ana@pxe-server:~$
sudo iptables -A INPUT -i classroom -p udp --dport 69 -j DROP
```

### The new PC that won't boot

```sh
# ana@pxe-server:~$
sudo journalctl -u dnsmasq -o cat | grep -m1 'Arch:00000'
sudo journalctl -u dnsmasq -o cat --since 23:31:50 | grep -E 'vendor class|DHCPACK'
cat /etc/dnsmasq.d/pxe.conf
```

### Why big files moved to HTTP

```sh
# ana@pxe-server:~$
sudo tc qdisc add dev classroom root netem delay 10ms
cat /srv/tftp/pxelinux.cfg/default
grep dhcp-boot /etc/dnsmasq.d/pxe.conf
sudo tail -n 2 /var/log/nginx/access.log
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
