# Ana's tractor dealership web server for P126: a stock Ubuntu 24.04 with systemd as PID 1, Ubuntu's own nginx (the
# web server in front) and her Django site in a virtual environment with Django, gunicorn and WhiteNoise from PyPI
# (pinned). Ana is the first user (groups adm and sudo, as on a real install; sudo without a password so the pty demo
# needs no typed password). The demo writes the gunicorn service and nginx's site file.
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends systemd systemd-sysv dbus sudo curl nginx \
      python3 python3-venv procps iproute2 less nano ca-certificates tree \
 && rm -f /usr/sbin/policy-rc.d \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash -G adm,sudo ana \
 && echo 'ana ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/ana && chmod 440 /etc/sudoers.d/ana \
 && rm -f /etc/nginx/sites-enabled/default \
 && systemctl mask getty@tty1.service console-getty.service
COPY --chown=ana:ana tractors /home/ana/tractors
RUN su - ana -c 'cd tractors && python3 -m venv .venv && .venv/bin/pip install -q --no-cache-dir \
      Django==6.1.3 gunicorn==27.0.1 whitenoise==6.12.0'
STOPSIGNAL SIGRTMIN+3
CMD ["/sbin/init"]
