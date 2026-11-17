# How SNMP Network Monitoring Works

Video: https://youtu.be/MAlORrScoPw  
Written version: https://cloudexplainers.com/how-snmp-network-monitoring-works/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/wan-rate`](lab/wan-rate)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### No login, still an answer

```sh
# ana@office:~$
wan-rate 4
```

### A stock agent answers no one

```sh
# ana@office:~$
snmpget -v2c -c public router 1.3.6.1.2.1.1.5.0
# ana@router:~$
sudo ss -ulpn | grep :161
sudo systemctl restart snmpd
sudo ss -ulpn | grep :161
# ana@office:~$
snmpget -v2c -c public router 1.3.6.1.2.1.1.5.0
```

### The long number is an address

```sh
# ana@office:~$
snmptranslate -m SNMPv2-MIB 1.3.6.1.2.1.1.5.0
echo 'mibs +SNMPv2-MIB:IF-MIB:HOST-RESOURCES-MIB' | sudo tee -a /etc/snmp/snmp.conf
snmpget -v2c -c public router sysName.0 hrSystemUptime.0
```

### Who may read what

```sh
# ana@office:~$
snmpwalk -v2c -c public router IF-MIB::ifDescr
# ana@router:~$
sudo grep -E '^(view|rocommunity)' /etc/snmp/snmpd.conf
sudo grep -E '^(rocommunity|trap2sink|authtrapenable)' /etc/snmp/snmpd.conf
sudo systemctl restart snmpd
# ana@office:~$
snmpwalk -v2c -c brew-mon router IF-MIB::ifDescr
```

### Speed is two readings

```sh
# ana@office:~$
snmpget -v2c -c brew-mon router IF-MIB::ifHCInOctets.12; sleep 10; snmpget -v2c -c brew-mon router IF-MIB::ifHCInOctets.12
```

### The wrong community

```sh
# ana@office:~$
snmpget -v2c -c public router sysName.0
journalctl -u snmptrapd -o cat -n 4
```

### Who else can read it

```sh
# ana@router:~$
sudo tcpdump -n -v -c 1 -i lan udp port 161
# ana@office:~$
snmpget -v2c -c brew-mon router sysName.0
# ana@router:~$
sudo systemctl stop snmpd && sudo net-snmp-create-v3-user -ro -a SHA-256 -A Hop-Kettle-42 -x AES -X Mash-Tun-77 ana && sudo systemctl start snmpd
# ana@office:~$
snmpget -v3 -l authPriv -u ana -a SHA-256 -A Hop-Kettle-42 -x AES -X Mash-Tun-77 router sysName.0
# ana@router:~$
sudo tcpdump -n -v -c 3 -i lan udp port 161
```

### The router speaks first

```sh
# ana@router:~$
date +%T; sudo ip link set wan down
# ana@office:~$
journalctl -u snmptrapd -o cat -n 7
journalctl -u snmptrapd -o cat -n 7
```

### One manager, every device

```sh
# ana@office:~$
for h in router brewhouse; do snmpget -v2c -c brew-mon $h sysName.0 hrSystemUptime.0; done
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
