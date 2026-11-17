# P142's lab image: a stock Ubuntu 24.04 with systemd as PID 1, for the two machines of an ice rink's small network.
#   target "db":  rink-db, the rink's database server with Ubuntu's own PostgreSQL 16, as installed: it listens on
#                 localhost only and pg_hba.conf has no line for other machines yet.
#   target "web": rink-web, the booking website (rink/app.py, Python's http.server + psycopg2) as a systemd service
#                 on port 8080, and the psql client.
# Ana is the first user (groups adm and sudo, as on a real install; sudo without a password so the pty demo needs no
# typed password).
FROM ubuntu:24.04 AS base
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends systemd systemd-sysv dbus sudo curl iproute2 \
      iputils-ping ufw procps less nano ca-certificates postgresql-client python3 python3-psycopg2 \
 && rm -f /usr/sbin/policy-rc.d \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash -G adm,sudo ana \
 && echo 'ana ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/ana && chmod 440 /etc/sudoers.d/ana \
 && touch /home/ana/.hushlogin \
 && sed -i "s/^IPV6=yes/IPV6=no/" /etc/default/ufw \
 && systemctl mask getty@tty1.service console-getty.service
STOPSIGNAL SIGRTMIN+3
CMD ["/sbin/init"]

FROM base AS db
RUN apt-get update && apt-get install -y --no-install-recommends postgresql

FROM base AS web
COPY rink/app.py /srv/rink/app.py
COPY rink/rink.service /etc/systemd/system/rink.service
RUN mkdir -p /etc/rink && systemctl enable rink.service
