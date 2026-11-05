# Linux Cron Jobs Will Finally Make Sense After This

Video: https://youtu.be/imWZStwvHEQ  
Written version: https://cloudexplainers.com/linux-cron-jobs-will-finally-make-sense-after-this/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/backup.sh`](lab/backup.sh)
- [`lab/orders.txt`](lab/orders.txt)
- [`lab/shop-export`](lab/shop-export)

## Commands, in the order the video runs them

### A backup that never ran

```sh
# ana@shop:~$
cat backup.sh
./backup.sh
```

### Reading a schedule

```sh
# ana@shop:~$
crontab -l
cat cron.txt
crontab cron.txt
```

### Where the error went

```sh
# ana@shop:~$
date; ls backups
journalctl -u cron --no-pager | grep -v pam_unix
cat cron.txt
crontab cron.txt
cat backup.log
```

### Cron's small world

```sh
# ana@shop:~$
cat cron-env.txt
echo $PATH
cat cron.txt
crontab cron.txt
cat backup.log
ls backups
```

### The percent sign

```sh
# ana@shop:~$
cat cron.txt
crontab cron.txt
ls logs backups
journalctl -u cron --no-pager | grep -v pam_unix | tail -n 2
cat cron.txt
crontab cron.txt
ls logs
cat logs/backup-*.log
```

### Time traps

```sh
# ana@shop:~$
timedatectl | grep 'Time zone'
date; TZ=America/New_York date
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
