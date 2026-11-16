# P136's database server, "lessons": a stock Ubuntu 24.04 with systemd as PID 1 and Ubuntu's own PostgreSQL 16,
# standing in for a music school's server. PostgreSQL listens on every address, and one pg_hba.conf line lets the
# school's office network log in with a password (scram-sha-256), as Ubuntu's own localhost lines do.
# Ana is the first user (groups adm and sudo; sudo without a password so the pty demo needs no typed password).
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends systemd systemd-sysv dbus sudo postgresql \
      iproute2 procps less nano ca-certificates \
 && rm -f /usr/sbin/policy-rc.d \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash -G adm,sudo ana \
 && echo 'ana ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/ana && chmod 440 /etc/sudoers.d/ana \
 && touch /home/ana/.hushlogin \
 && echo "listen_addresses = '*'" > /etc/postgresql/16/main/conf.d/listen.conf \
 && printf '\n# The school office\nhost    all             all             192.168.70.0/24         scram-sha-256\n' \
      >> /etc/postgresql/16/main/pg_hba.conf \
 && systemctl mask getty@tty1.service console-getty.service
STOPSIGNAL SIGRTMIN+3
CMD ["/sbin/init"]
