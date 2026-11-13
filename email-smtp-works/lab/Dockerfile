# One image for every machine in P106's mail lab: a stock Ubuntu 24.04 with the archive's Postfix (sends and receives
# mail over SMTP), Dovecot (logins and IMAP), dnsmasq (the lab's DNS), swaks (sends one email from a terminal),
# curl (reads mail over IMAP) and the usual network tools. A small lab certificate authority signs both mail servers'
# certificates, and every machine trusts it, as real machines trust the public authorities.
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN echo "postfix postfix/main_mailer_type select Internet Site" | debconf-set-selections \
 && echo "postfix postfix/mailname string localhost" | debconf-set-selections \
 && apt-get update && apt-get install -y --no-install-recommends postfix postfix-policyd-spf-python dovecot-core \
      dovecot-imapd dnsmasq swaks telnet libnet-ssleay-perl libio-socket-ssl-perl libterm-readkey-perl curl bind9-dnsutils netcat-openbsd iproute2 iputils-ping openssl ca-certificates \
      sudo less nano procps \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash -G sudo ana && useradd -m -s /bin/bash -G sudo ben && useradd -m -s /bin/bash cara \
 && echo '%sudo ALL=(ALL) NOPASSWD: ALL' > /etc/sudoers.d/lab \
 && echo 'Defaults !admin_flag' >> /etc/sudoers.d/lab \
 && touch /home/ana/.sudo_as_admin_successful /home/ben/.sudo_as_admin_successful
COPY .ca /lab/ca
RUN cp /lab/ca/lab-ca.crt /usr/local/share/ca-certificates/ && update-ca-certificates >/dev/null
CMD ["sleep", "infinity"]
