# Proxmox vs ESXi for Your Homelab: When Each One Wins

Video: https://youtu.be/GOLaQcEzW30  
Written version: https://cloudexplainers.com/proxmox-vs-esxi-for-your-homelab-when-each-one-wins/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/mkvm.sh`](lab/mkvm.sh)

## Commands, in the order the video runs them

### One network card, two installers

```sh
# root@pve-lab:~#
lspci -k -s 02:00.0
```

### Where the VMs go

```sh
# root@pve-lab:~#
pvesm status
```

### What it costs

```sh
# root@pve-lab:~#
apt update
cat /etc/apt/sources.list.d/proxmox.sources
apt update
```

### Containers

```sh
# root@pve-lab:~#
pct create 101 local:vztmpl/debian-13-standard_13.6-1_amd64.tar.zst --hostname photos --memory 512 --rootfs local-lvm:4 --net0 name=eth0,bridge=vmbr0,ip=dhcp --unprivileged 1 --features nesting=1 >/dev/null && echo created
time pct start 101
pct exec 101 -- free -m
```

### Backups

```sh
# root@pve-lab:~#
vzdump 101 --storage local --mode snapshot --compress zstd 2>&1 | grep -E 'Finished Backup|archive file size|Backup job finished'
ls -lh /var/lib/vz/dump/ | grep tar
```

### Automation

```sh
# ana@laptop:~/homelab$
curl -sk -H "Authorization: PVEAPIToken=$TOKEN" -d vmid=200 -d name=media -d memory=1024 https://pve-lab:8006/api2/json/nodes/pve-lab/qemu
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
