# SSH on Linux: Full Tutorial for Beginners

Video: https://youtu.be/-ERKMa89EFU  
Written version: https://cloudexplainers.com/ssh-on-linux-full-tutorial-for-beginners/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/board/board.service`](lab/board/board.service)
- [`lab/board/www/index.html`](lab/board/www/index.html)
- [`lab/board/www/today.txt`](lab/board/www/today.txt)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### One line, no password

```sh
# kari@laptop:~$
ssh tower 'hostname; tail -1 /srv/board/www/today.txt'
# kari@tower:~$
sudo journalctl -u ssh --no-pager -o cat | grep Accepted | tail -1
```

### Installing the SSH server

```sh
# kari@laptop:~$
ssh kari@tower
# kari@tower:~$
systemctl status ssh --no-pager
sudo apt install -y openssh-server
sudo ss -tlnp | grep ':22 '
```

### The first connection

```sh
# kari@laptop:~$
ssh kari@tower
# kari@tower:~$
ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub
hostname
who
exit
# kari@laptop:~$
cut -d' ' -f1,2 ~/.ssh/known_hosts
ssh kari@tower df -h /
```

### SSH keys

```sh
# kari@laptop:~$
ssh-keygen -t ed25519
ls -l ~/.ssh/id_*
cat ~/.ssh/id_ed25519.pub
ssh-copy-id kari@tower
# kari@tower:~$
cat ~/.ssh/authorized_keys
ls -ld ~/.ssh ~/.ssh/authorized_keys
# kari@laptop:~$
ssh kari@tower hostname
ssh -v kari@tower true 2>&1 | grep -E 'Offering|accepts|Authenticated to'
# kari@tower:~$
sudo journalctl -u ssh --no-pager -o cat | grep Accepted
# kari@laptop:~$
ssh-keygen -lf ~/.ssh/id_ed25519.pub
chmod 644 ~/.ssh/id_ed25519
ssh kari@tower hostname
chmod 600 ~/.ssh/id_ed25519
```

### Typing the passphrase once

```sh
# kari@laptop:~$
eval "$(ssh-agent)"
ssh-add
ssh-add -l
ssh kari@tower uptime
```

### Shortcuts in ~/.ssh/config

```sh
# kari@laptop:~$
cat ~/.ssh/config
ssh tower
# kari@tower:~$
hostname
exit
# kari@laptop:~$
ssh tower hostname; hostname
ssh tower 'hostname; uptime -p'
```

### When a key stops working

```sh
# kari@tower:~$
chmod o+w ~
# kari@laptop:~$
ssh tower hostname
# kari@tower:~$
sudo journalctl -u ssh --no-pager -o cat | grep 'bad ownership' | tail -1
chmod o-w ~
# kari@laptop:~$
ssh tower hostname
```

### Copying files

```sh
# kari@laptop:~$
scp tower:/srv/board/www/today.txt .
cat today.txt
du -sh logbook && ls logbook | wc -l
rsync -a --stats logbook tower: | grep -E 'transferred:|^sent'
rsync -a --stats logbook tower: | grep -E 'transferred:|^sent'
rsync -a --stats logbook tower: | grep -E 'transferred:|^sent'
```

### Jobs that outlive the connection

```sh
# kari@tower:~$
./backup.sh &
tail -1 backup.log
# kari@laptop:~$
ssh tower 'tail -1 backup.log; date +%T; pgrep -c backup.sh'
# kari@tower:~$
tmux new -d -s backup ./backup.sh
tmux ls
# kari@laptop:~$
ssh tower 'tail -1 backup.log; date +%T; tmux ls'
```

### When the host key changes

```sh
# kari@tower:~$
ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub
# kari@laptop:~$
ssh tower hostname
ssh-keygen -R tower
ssh tower hostname
```

### Keys only: passwords off

```sh
# kari@laptop:~$
ssh tom@tower
# kari@tower:~$
cat /etc/ssh/sshd_config.d/10-airfield.conf
sudo sshd -t
sudo sshd -t && echo config OK
sudo systemctl reload ssh
sudo sshd -T | grep -E '^(passwordauthentication|permitrootlogin|pubkeyauthentication) '
# kari@laptop:~$
ssh tom@tower
ssh tower hostname
```

### Reaching a page through the tunnel

```sh
# kari@tower:~$
curl -s localhost:8080/today.txt
sudo ss -tlnp | grep 8080
# kari@laptop:~$
curl -sS tower:8080/today.txt
ssh -f -N -L 8080:localhost:8080 tower
curl -s localhost:8080/today.txt
ps -o pid,args -C ssh
kill 273
curl -sS localhost:8080/today.txt
```

### Jumping through the tower

```sh
# kari@laptop:~$
ssh fuel hostname
ssh -J tower kari@fuel
# kari@fuel:~$
hostname
exit
# kari@laptop:~$
cat ~/.ssh/config
ssh-copy-id fuel
ssh fuel hostname
```

### A firewall that keeps SSH open

```sh
# kari@tower:~$
sudo ufw allow OpenSSH
sudo ufw enable
sudo ufw status
exit
# kari@laptop:~$
ssh tower hostname
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
