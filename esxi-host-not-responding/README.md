# How to Fix a Homelab ESXi Host Not Responding

Video: https://youtu.be/KvJwz6TSKJs  
Written version: https://cloudexplainers.com/how-to-fix-a-homelab-esxi-host-not-responding/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/overlay/etc/apk/world`](lab/overlay/etc/apk/world)
- [`lab/overlay/etc/hostname`](lab/overlay/etc/hostname)
- [`lab/overlay/runlevels.txt`](lab/overlay/runlevels.txt)

## Commands, in the order the video runs them

### Ping works, the page doesn't

```sh
# ana@laptop:~$
ping -c 10 192.168.1.71
curl -skS -o /dev/null -w '%{http_code} after %{time_total}s\n' https://192.168.1.71/ui/ --max-time 200
curl -s http://192.168.1.73/ | grep -o '<h1>.*</h1>'
```

### The host agent

```sh
# ana@laptop:~$
curl -skS -o /dev/null -w '%{http_code} after %{time_total}s\n' https://192.168.1.71/ui/
curl -s http://192.168.1.73/ | grep -o '<h1>.*</h1>'
```

### No ping: a new address

```sh
# ana@laptop:~$
ping -c 3 192.168.1.71
curl -skS -o /dev/null -w '%{http_code} after %{time_total}s\n' https://192.168.1.71/ui/ --max-time 20
curl -s http://192.168.1.73/ | grep -o '<h1>.*</h1>'
curl -skS -o /dev/null -w '%{http_code} after %{time_total}s\n' https://192.168.1.71/ui/
```

### Right address, still silent

```sh
# ana@laptop:~$
ping -c 3 192.168.1.71
curl -s http://192.168.1.73/ | grep -o '<h1>.*</h1>'
```

### The rare one

```sh
# ana@laptop:~$
ping -c 3 192.168.1.71
curl -sS --max-time 10 http://192.168.1.73/ | grep -o '<h1>.*</h1>'
curl -s http://192.168.1.73/ | grep -o '<h1>.*</h1>'
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
