# Linux Users and Groups Will Finally Make Sense

Video: https://youtu.be/5uKIGLDzg4I  
Written version: https://cloudexplainers.com/linux-users-and-groups-will-finally-make-sense/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Commands, in the order the video runs them

### Permission denied

```sh
# ana@ubuntu:~$
id ben
# ben@ubuntu:~$
touch /srv/team/plan.txt
```

### Users: a name and a number

```sh
# ana@ubuntu:~$
whoami
id
tail -n 1 /etc/passwd
head -n 1 /etc/passwd
wc -l /etc/passwd
grep www-data /etc/passwd
```

### Groups

```sh
# ana@ubuntu:~$
grep ana /etc/group
groups
```

### Creating users and groups

```sh
# ana@ubuntu:~$
sudo useradd -m -s /bin/bash ben
sudo passwd ben
id ben
sudo groupadd team
sudo mkdir /srv/team
sudo usermod -aG team ben
grep team /etc/group
```

### Owners and permissions

```sh
# ana@ubuntu:~$
ls -ld /srv/team
sudo chgrp team /srv/team
sudo chmod g+w /srv/team
ls -ld /srv/team
ls -lnd /srv/team
```

### Why Ben was denied

```sh
# ben@ubuntu:~$
id
su - ben
id
touch /srv/team/plan.txt
ls -l /srv/team
```

### The -a trap

```sh
# ana@ubuntu:~$
sudo usermod -G users ben
id ben
sudo usermod -aG team ben
id ben
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
