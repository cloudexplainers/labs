# The 5 Levels of Linux Boot: From Power On to Login

Video: https://youtu.be/1jbzbH0tcW8  
Written version: https://cloudexplainers.com/the-5-levels-of-linux-boot-from-power-on-to-login/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Commands, in the order the video runs them

### Level 1: Firmware

```sh
# ana@ubuntu:~$
ls /sys/firmware/efi
sudo efibootmgr
sudo ls /boot/efi/EFI/ubuntu
```

### Level 2: Bootloader

```sh
# ana@ubuntu:~$
ls /boot
cat /proc/cmdline
```

### Level 3: Kernel

```sh
# ana@ubuntu:~$
sudo dmesg | grep -E 'Linux version|Memory: |smpboot: Total|Run /init' | cut -c1-70
lsmod | wc -l
```

### Level 4: initramfs

```sh
# ana@ubuntu:~$
ls -lh /boot/initrd.img-* /boot/vmlinuz-*
sudo lsinitramfs /boot/initrd.img | wc -l
lsblk -o NAME,FSTYPE,SIZE,UUID,MOUNTPOINTS /dev/vda
(initramfs) cat /proc/cmdline
(initramfs) ls /dev/disk/by-uuid
```

### Level 5: systemd

```sh
# ana@ubuntu:~$
ps -p 1 -o pid,comm
systemctl get-default
systemd-analyze
systemd-analyze blame | head -n 5
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
