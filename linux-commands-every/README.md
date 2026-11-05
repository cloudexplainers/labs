# Every Linux Command You Actually Need

Video: https://youtu.be/BcaoTwHAoPQ  
Written version: https://cloudexplainers.com/every-linux-command-you-actually-need/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Commands, in the order the video runs them

### The terminal

```sh
# ana@ubuntu:~$
du -sh * | sort -rh | head -n 3
ls -l Documents
```

### Navigate: pwd, ls, cd

```sh
# ana@ubuntu:~$
pwd
ls
ls -a
ls -l
cd projects/website
# ana@ubuntu:~/projects/website$
ls
cd ..
# ana@ubuntu:~/projects$
pwd
cd
# ana@ubuntu:~$
pwd
```

### Files: mkdir, cp, mv, rm

```sh
# ana@ubuntu:~$
mkdir backups
touch todo.txt
ls
cp notes.txt backups/
ls backups
mv todo.txt tasks.txt
ls
rm tasks.txt
rm backups
rm -r backups
ls
```

### Read: cat, head, tail

```sh
# ana@ubuntu:~$
cat notes.txt
wc -l app.log
head -n 3 app.log
tail -n 3 app.log
```

### Search: grep, find

```sh
# ana@ubuntu:~$
grep "disk full" app.log
grep -c ERROR app.log
find . -name "*.txt"
find . -size +100M
```

### Pipes and redirection

```sh
# ana@ubuntu:~$
grep ERROR app.log | wc -l
du -sh *
du -sh * | sort -rh
grep ERROR app.log > errors.txt
wc -l errors.txt
echo "Call the bank" >> notes.txt
cat notes.txt
```

### Permissions: chmod, sudo

```sh
# ana@ubuntu:~$
ls -l backup.sh
./backup.sh
chmod +x backup.sh
ls -l backup.sh
./backup.sh
whoami
cat /etc/shadow
sudo whoami
```

### Processes: ps, kill

```sh
# ana@ubuntu:~$
ps aux --sort=-%cpu | head -n 3
kill 125
ps aux --sort=-%cpu | head -n 3
```

### Disk and memory: df, du, free

```sh
# ana@ubuntu:~$
df -h /
free -h
```

### Install and network: apt, curl, ping

```sh
# ana@ubuntu:~$
curl -I https://example.com
sudo apt install -y curl
sudo apt update
sudo apt install -y curl iputils-ping
curl -I https://example.com
ping -c 3 1.1.1.1
```

### Help: --help, man, history

```sh
# ana@ubuntu:~$
ls --help | head -n 4
man ls
history | tail -n 5
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
