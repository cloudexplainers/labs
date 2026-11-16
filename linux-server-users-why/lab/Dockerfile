# P145's lab image: a stock Ubuntu 24.04 with systemd as PID 1, used for three machines of a farmers market's
# small setup: "market" (the server: nginx, the order app under gunicorn, SQLite), "payments" (a stand-in card
# payment service that answers in 200 ms) and "laptop" (Ana's laptop with wrk, the load tester). Ana is the first
# user (groups adm and sudo; sudo without a password so the pty demo needs no typed password).
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends systemd systemd-sysv dbus sudo curl python3 \
      python3-flask gunicorn nginx-light sqlite3 wrk iproute2 procps less nano ca-certificates \
 && rm -f /usr/sbin/policy-rc.d \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash -G adm,sudo ana \
 && echo 'ana ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/ana && chmod 440 /etc/sudoers.d/ana \
 && touch /home/ana/.hushlogin \
 && rm -f /etc/nginx/sites-enabled/default \
 && systemctl mask getty@tty1.service console-getty.service
COPY market/ /srv/market/
COPY payments.py /srv/payments.py
COPY payments.service /etc/systemd/system/payments.service
COPY idle.py /home/ana/idle.py
COPY memused cpuused /usr/local/bin/
RUN python3 /srv/market/make_db.py && rm /srv/market/make_db.py \
 && mv /srv/market/nginx.conf /etc/nginx/nginx.conf && mv /srv/market/market.service /etc/systemd/system/ \
 && echo 'wrk.method = "POST"' > /home/ana/post.lua \
 && chown -R ana:ana /home/ana && chown -R ana:www-data /srv/market && chmod -R g+rX /srv/market
STOPSIGNAL SIGRTMIN+3
CMD ["/sbin/init"]
