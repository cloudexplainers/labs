# The 7 Levels of Cybersecurity

Video: https://youtu.be/osWorSTbpB4  
Written version: https://cloudexplainers.com/the-7-levels-of-cybersecurity/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Commands, in the order the video runs them

### The 7 levels

```sh
python3 pwned.py password123 sunshine 'Summer2024!' gatherer-ongoing-comfy-proton-gestate
```

### Level 1: Passwords

```sh
echo -n sunshine | sha256sum
echo -n sunshinE | sha256sum
python3 guess_speed.py
```

### Level 2: MFA

```sh
python3 mfa.py
```

### Level 3: Phishing

```sh
python3 lookalike.py
```

### Level 4: Updates

```sh
curl -s https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json | jq .count
trivy image -q --severity HIGH,CRITICAL python:3.9.0-slim | grep -B2 Total
trivy image -q --severity HIGH,CRITICAL python:3.13-slim | grep -B2 Total
```

### Level 5: Encryption

```sh
curl -s -d 'user=ana&password=hunter2' http://web/login
tcpdump -A -r http.pcap 2>/dev/null | grep -a password
curl -s -d 'user=ana&password=hunter2' --cacert /certs/ca.pem https://web/login
tcpdump -A -r https.pcap 2>/dev/null | grep -a -c password
curl -sv --cacert /certs/ca.pem -d x=1 https://web/login 2>&1 | grep 'SSL connection'
```

### Level 6: Least privilege

```sh
GRANT SELECT ON customers TO reporting;
reporting=> SELECT count(*) FROM customers;
reporting=> DELETE FROM customers;
nmap -Pn -p 80,5432,6379 server
iptables -A INPUT -p tcp --dport 80 -j ACCEPT && iptables -A INPUT -p tcp -m multiport --dports 5432,6379 -j DROP && iptables -S INPUT
nmap -Pn -p 80,5432,6379 server
```

### Level 7: Detection

```sh
for pw in 123456 password qwerty letmein admin iloveyou welcome monkey; do sshpass -p $pw ssh -o StrictHostKeyChecking=no -o ConnectTimeout=3 ana@ssh-server true 2>&1 | tail -1 | sed "s/^/$pw: /"; sleep 1; done
grep 'Failed password' /var/log/auth.log | tail -3
fail2ban-client status sshd
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
