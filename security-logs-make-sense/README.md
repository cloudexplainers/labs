# Security Logs Will Finally Make Sense After This

Video: https://youtu.be/Fsi7Imyo6Ts  
Written version: https://cloudexplainers.com/security-logs-will-finally-make-sense-after-this/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/bot`](lab/bot)
- [`lab/passwords.txt`](lab/passwords.txt)

## Commands, in the order the video runs them

### A break-in, in the logs

```sh
# thief@thief-pc:~$
./bot shop
# ana@shop:~$
sudo tail -n 8 /var/log/auth.log
```

### Reading the attack

```sh
# ana@shop:~$
grep -c "Failed password" /var/log/auth.log
grep "Failed password" /var/log/auth.log | grep -o "from [0-9.]*" | sort | uniq -c
grep "Failed password" /var/log/auth.log | grep -oE "for (invalid user )?[a-z]+" | sort | uniq -c | sort -rn
```

### The line that matters

```sh
# ana@shop:~$
grep Accepted /var/log/auth.log
journalctl -u ssh -g Accepted --no-pager
last -i test
grep "NOT in sudoers" /var/log/auth.log
```

### The web server's log

```sh
# ana@shop:~$
tail -n 8 /var/log/nginx/access.log
```

### Acting on the logs

```sh
# ana@shop:~$
sudo usermod --lock --expiredate 1 test
sudo passwd -S test
sudo systemctl enable --now fail2ban
sudo fail2ban-client status sshd
# thief@thief-pc:~$
./bot shop
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
