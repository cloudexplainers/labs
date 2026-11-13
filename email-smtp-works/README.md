# How Email Works on the Internet (SMTP) in 10 Minutes

Video: https://youtu.be/TdhWvaZ5Ob4  
Written version: https://cloudexplainers.com/how-email-works-on-the-internet-smtp-in-10-minutes/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/conf/dnsmasq.conf`](lab/conf/dnsmasq.conf)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### Press send

```sh
# ana@ana-laptop:~$
swaks --to ben@harbor.test --h-Subject 'Flowers for Saturday' --body '12 sunflowers, at the cafe by 8 am. Ana'
# ben@ben-laptop:~$
curl -sn --ssl-reqd 'imap://mx.harbor.test/INBOX;MAILINDEX=1'
```

### Why Ana logs in

```sh
# ana@ana-laptop:~$
telnet mail.bloom.test 25
```

### Who takes mail for harbor.test?

```sh
# ana@mail:~$
dig +short MX harbor.test
dig +short mx.harbor.test
grep 'to=<ben@harbor.test>' /var/log/mail.log
```

### The conversation

```sh
# ana@mail:~$
telnet mx.harbor.test 25
```

### Envelope and letter

```sh
# ana@ana-laptop:~$
swaks --to ben@harbor.test,cara@harbor.test --h-To ben@harbor.test --h-Subject 'March invoice' --body 'Invoice attached. Ana'
# ben@mx:~$
grep -E 'to=<(ben|cara)@harbor.test>' /var/log/mail.log | tail -2 | cut -d' ' -f6-
```

### When the other server is off

```sh
# ana@ana-laptop:~$
swaks --to ben@harbor.test --h-Subject 'Change of plan' --body 'Make it 20 sunflowers. Ana'
# ana@mail:~$
mailq
postconf maximal_queue_lifetime
sudo postqueue -f
mailq
```

### Reading it: IMAP

```sh
# ben@ben-laptop:~$
curl -sn --ssl-reqd imap://mx.harbor.test/INBOX -X 'SEARCH ALL'
curl -sn --ssl-reqd 'imap://mx.harbor.test/INBOX;MAILINDEX=4' | grep -E '^(Subject|Date):'
```

### Is it really from Bloom?

```sh
# ana@mail:~$
dig +short TXT bloom.test
# ben@ben-laptop:~$
curl -sn --ssl-reqd 'imap://mx.harbor.test/INBOX;MAILINDEX=1' | grep -A1 '^Received-SPF'
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
