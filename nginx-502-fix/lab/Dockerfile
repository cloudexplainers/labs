# Ana's climbing gym server for P127: a stock Ubuntu 24.04 with systemd as PID 1, Ubuntu's own nginx (the web
# server in front) and Ubuntu's own gunicorn (the Python app server behind it). Ana is the first user (groups adm and
# sudo, as on a real install; sudo without a password so the pty demo needs no typed password). Her booking app is
# copied into ~/booking and started as a systemd service by the demo, which also writes nginx's site file.
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends systemd systemd-sysv dbus sudo curl nginx gunicorn \
      python3 procps iproute2 less nano ca-certificates \
 && rm -f /usr/sbin/policy-rc.d \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash -G adm,sudo ana \
 && echo 'ana ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/ana && chmod 440 /etc/sudoers.d/ana \
 && rm -f /etc/nginx/sites-enabled/default \
 && systemctl mask getty@tty1.service console-getty.service
STOPSIGNAL SIGRTMIN+3
CMD ["/sbin/init"]
