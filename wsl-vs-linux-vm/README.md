# WSL vs a Linux Virtual Machine: Which One Should You Use?

Video: https://youtu.be/ERrf1qwEYSE  
Written version: https://cloudexplainers.com/wsl-vs-a-linux-virtual-machine-which-one-should-you-use/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/shop/index.html`](lab/shop/index.html)

## Commands, in the order the video runs them

### Two kinds of Linux on one PC

```sh
PS C:\Users\mike> wsl -l -v
PS C:\Users\mike> wsl uname -r
PS C:\Users\mike> ssh mike@192.168.1.202 uname -r
```

### Files on the C drive

```sh
# mike@flowershop-pc:~$
mkdir ~/orders && cd ~/orders && time (for i in $(seq 1 2000); do echo "roses" > order$i.txt; done)
mkdir /mnt/c/Users/mike/orders && cd /mnt/c/Users/mike/orders && time (for i in $(seq 1 2000); do echo "roses" > order$i.txt; done)
# mike@shop-server:~$
ls /mnt/c
```

### Can the tablet reach it?

```sh
# mike@flowershop-pc:~$
cd ~/shop && python3 -m http.server 8000 &
PS C:\Users\mike> curl.exe -s -o NUL -w "%{http_code}" http://localhost:8000
# trish@tablet:~$
curl -m 10 http://192.168.1.53:8000
PS C:\Users\mike> Get-NetTCPConnection -LocalPort 8000 -State Listen | ft LocalAddress,LocalPort
PS C:\Users\mike> netsh interface portproxy add v4tov4 listenport=8000 listenaddress=0.0.0.0 connectport=8000 connectaddress=172.19.26.255
PS C:\Users\mike> New-NetFirewallRule -DisplayName 'Shop page 8000' -Direction Inbound -Protocol TCP -LocalPort 8000 -Action Allow | ft DisplayName,Enabled,Action
# trish@tablet:~$
curl -s http://192.168.1.53:8000 | grep -o '<title>.*</title>'
# mike@shop-server:~$
ip -4 -br addr show eth0
systemctl is-active shop
# trish@tablet:~$
curl -s http://192.168.1.202:8000 | grep -o '<title>.*</title>'
```

### After a restart

```sh
PS C:\Users\mike> Restart-Computer
# trish@tablet:~$
curl -s http://192.168.1.202:8000 | grep -o '<title>.*</title>'
curl -m 10 http://192.168.1.53:8000
PS C:\Users\mike> wsl -l -v
PS C:\Users\mike> Get-VM shop-server
# mike@shop-server:~$
uptime -p
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
