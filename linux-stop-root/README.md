# Stop Running Linux as Root (Do This Instead)

Video: https://youtu.be/D8d7v9MhOA0  
Written version: https://cloudexplainers.com/stop-running-linux-as-root-do-this-instead/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Commands, in the order the video runs them

### One command, as root

```sh
# root@ubuntu:/srv/team#
ls -l
rm -rf *
ls -l
# ana@ubuntu:/srv/team$
rm -rf *
```

### What root is

```sh
# ana@ubuntu:~$
id
sudo -i
# root@ubuntu:~#
id
ps -o user,pid,comm
```

### Root's files in your home

```sh
# root@ubuntu:/srv/team#
cd /home/ana
# root@ubuntu:/home/ana#
echo 'renew the certificates' > todo.txt
exit
# ana@ubuntu:~$
echo 'update the docs' >> todo.txt
ls -l todo.txt
```

### Do this instead: sudo

```sh
# ana@ubuntu:~$
sudo -k
sudo id
id
sudo chown ana:ana todo.txt
ls -l todo.txt
echo 'update the docs' >> todo.txt
cat todo.txt
```

### The redirect trap

```sh
# ana@ubuntu:~$
cat /etc/hosts
sudo echo '192.0.2.10 fileserver' >> /etc/hosts
echo '192.0.2.10 fileserver' | sudo tee -a /etc/hosts
tail -n 1 /etc/hosts
```

### The safety net

```sh
# ana@ubuntu:/srv/team$
ls -ld /srv/team
ls -l
```

### Why root is locked

```sh
# ana@ubuntu:~$
su -
sudo passwd -S root
grep sudo /etc/group
# ben@ubuntu:~$
sudo id
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
