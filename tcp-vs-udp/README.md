# TCP vs UDP: When Each One Wins

Video: https://youtu.be/KGZg0VVxaGI  
Written version: https://cloudexplainers.com/tcp-vs-udp-when-each-one-wins/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/call.py`](lab/call.py)
- [`lab/sendfile.py`](lab/sendfile.py)

## Commands, in the order the video runs them

### Round 1: Saying hello

```sh
# ana@laptop:~$
ping -c 3 server.example
ping -c 3 server.example
curl -s -o /dev/null -w 'name found: %{time_namelookup} s\nconnected:  %{time_connect} s\npage:       %{time_total} s\n' server.example
time dig +short server.example
time dig +tcp +short server.example
# root@cafe-router:~#
tcpdump -n -i lan -q port 53
tcpdump -n -i lan -q port 53
```

### Round 2: Every byte

```sh
# root@cafe-router:~#
tc qdisc change dev lan root netem delay 50ms loss 2%
tc qdisc change dev wan root netem delay 50ms loss 2%
# ana@laptop:~$
sha256sum photo.jpg
python3 sendfile.py send tcp photo.jpg server.example
# root@server:~#
python3 sendfile.py receive tcp
sha256sum photo.jpg
# ana@laptop:~$
python3 sendfile.py send udp photo.jpg server.example
# root@server:~#
python3 sendfile.py receive udp
sha256sum photo.jpg
```

### Round 3: Right now

```sh
# ana@laptop:~$
python3 call.py send tcp server.example
# root@server:~#
python3 call.py listen tcp
# ana@laptop:~$
python3 call.py send udp server.example
# root@server:~#
python3 call.py listen udp
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
