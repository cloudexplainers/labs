# HTTP vs HTTPS: What Actually Changes on Your Network

Video: https://youtu.be/6aY4H3bnnBE  
Written version: https://cloudexplainers.com/http-vs-https-what-actually-changes-on-your-network/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Commands, in the order the video runs them

### HTTP on the wire

```sh
# sam@cafe-router:~$
sudo tcpdump -i wifi -w http.pcap port 80
# ana@laptop:~$
curl -d 'user=ana&password=Blue-Kettle-42' http://shop.example/login
# sam@cafe-router:~$
tshark -r http.pcap -Y http.request -T fields -E header=y -e ip.src -e http.host -e http.request.method -e http.request.uri | column -t
grep -aoE 'password=[A-Za-z0-9-]+|session=[0-9a-f]+|Welcome back, [a-z]+' http.pcap
```

### HTTPS on the wire

```sh
# sam@cafe-router:~$
sudo tcpdump -i wifi -w https.pcap port 443 or port 53
# ana@laptop:~$
curl -d 'user=ana&password=Blue-Kettle-42' https://shop.example/login
# sam@cafe-router:~$
tshark -r https.pcap
grep -acE 'password|session|Welcome' https.pcap
tshark -r https.pcap -Y http | wc -l
```

### What the café still sees

```sh
# sam@cafe-router:~$
tshark -r https.pcap -Y dns.a -T fields -E header=y -e dns.qry.name -e dns.a | column -t
tshark -r https.pcap -Y 'tls.handshake.type == 1' -T fields -E header=y -e ip.dst -e tcp.dstport -e tls.handshake.extensions_server_name | column -t
tshark -r https.pcap -Y 'tls.app_data' -T fields -E header=y -e ip.src -e frame.len | column -t
```

### Certificates and impostors

```sh
# ana@laptop:~$
curl -sv https://shop.example/ -o /dev/null 2>&1 | grep -E 'SSL connection|subject:|issuer:|expire date|verify ok'
grep -c 'BEGIN CERTIFICATE' /etc/ssl/certs/ca-certificates.crt
dig +short shop.example
curl -d 'user=ana&password=Blue-Kettle-42' http://shop.example/login
# eve@fake-shop:~$
cat stolen.txt
# ana@laptop:~$
curl -d 'user=ana&password=Blue-Kettle-42' https://shop.example/login
# eve@fake-shop:~$
cat stolen.txt
```

### What HTTPS costs

```sh
# ana@laptop:~$
ping -c 3 -q shop.example
curl -so /dev/null -w 'dns %{time_namelookup}  connect %{time_connect}  tls %{time_appconnect}  total %{time_total}\n' http://shop.example/
curl -so /dev/null -w 'dns %{time_namelookup}  connect %{time_connect}  tls %{time_appconnect}  total %{time_total}\n' https://shop.example/
openssl speed -seconds 1 -bytes 16384 -evp aes-256-gcm 2>/dev/null | tail -2
curl -so /dev/null -w 'dns %{time_namelookup}  connect %{time_connect}  tls %{time_appconnect}  total %{time_total}\n' https://shop.example/
```

### Making sites HTTPS only

```sh
# ana@laptop:~$
curl -sI http://shop.example/ | grep -E 'HTTP/|Location'
curl -sI https://shop.example/ | grep -E 'HTTP/|Strict'
curl -sL http://shop.example/
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
