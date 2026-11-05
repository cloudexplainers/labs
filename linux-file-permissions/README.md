# Every Linux File Permission You Need to Know

Video: https://youtu.be/t-R5_ckPpKI  
Written version: https://cloudexplainers.com/every-linux-file-permission-you-need-to-know/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Commands, in the order the video runs them

### Permission denied

```sh
# ana@ubuntu:~/shop$
./backup.sh
ls -l
```

### Files: read, write, run

```sh
# ana@ubuntu:~/shop$
chmod u+x backup.sh
ls -l backup.sh
./backup.sh
```

### Folders: list, change, enter

```sh
# ben@ubuntu:~$
ls /home/ana
cd /home/ana
# ana@ubuntu:~/shop$
ls -ld /home/ana
ls -l old.txt
echo 'new prices' >> old.txt
rm -f old.txt
ls
```

### chmod with letters

```sh
# ana@ubuntu:~/shop$
chmod g-w,o-r prices.txt
ls -l prices.txt
chmod u=rwx,go=rx backup.sh
ls -l backup.sh
```

### chmod with numbers

```sh
# ana@ubuntu:~/shop$
chmod 600 prices.txt
stat -c '%a %A %n' *
```

### chown and chgrp

```sh
# ana@ubuntu:~/shop$
chown ben prices.txt
chgrp team prices.txt
ls -l prices.txt
sudo mkdir /srv/shop
ls -ld /srv/shop
sudo chown ana:team /srv/shop
ls -ld /srv/shop
```

### umask: where files start

```sh
# ana@ubuntu:~/shop$
cd /srv/shop
# ana@ubuntu:/srv/shop$
umask
touch todo.txt price-list.txt
mkdir orders
ls -l
```

### setuid: run as the owner

```sh
# ben@ubuntu:~$
cat /etc/shadow
ls -l /etc/shadow
ls -l /usr/bin/passwd
passwd
```

### setgid: share a folder

```sh
# ben@ubuntu:~$
touch /srv/shop/ben.txt
# ana@ubuntu:/srv/shop$
chmod 2775 /srv/shop
ls -ld /srv/shop
# ben@ubuntu:~$
touch /srv/shop/ben.txt
# ana@ubuntu:/srv/shop$
ls -l
```

### The sticky bit

```sh
# ben@ubuntu:~$
rm -f /srv/shop/todo.txt
# ana@ubuntu:/srv/shop$
ls
ls -ld /tmp
chmod +t /srv/shop
ls -ld /srv/shop
# ben@ubuntu:~$
rm -f /srv/shop/price-list.txt
rm -f /srv/shop/ben.txt
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
