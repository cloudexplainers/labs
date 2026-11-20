# P124's lab image: a stock Ubuntu 24.04 with systemd as PID 1, as a small surf school's web server "surfschool".
# Ubuntu's own nginx serves two sites from it, the way a small business often runs them on one server:
#   www.surf.test  the booking page (static HTML + app.js)
#   api.surf.test  the lessons API, a small Flask app under gunicorn (surf-api.service), behind nginx
# Ana is the first user (groups adm and sudo, as on a real install; sudo without a password so the pty demo needs no
# typed password). Both names point at this server in /etc/hosts, so curl on the server reaches the same sites.
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends systemd systemd-sysv dbus sudo curl nginx \
      python3-flask gunicorn iproute2 procps less nano ca-certificates \
 && rm -f /usr/sbin/policy-rc.d \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash -G adm,sudo ana \
 && echo 'ana ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/ana && chmod 440 /etc/sudoers.d/ana \
 && touch /home/ana/.hushlogin \
 && systemctl mask getty@tty1.service console-getty.service \
 && rm -f /etc/nginx/sites-enabled/default
COPY site/ /var/www/surfschool/
COPY api/surf_api.py /srv/surf-api/surf_api.py
COPY api/surf-api.service /etc/systemd/system/surf-api.service
COPY nginx/surfschool.conf /etc/nginx/sites-available/surfschool.conf
COPY nginx/log.conf /etc/nginx/conf.d/log.conf
RUN ln -s /etc/nginx/sites-available/surfschool.conf /etc/nginx/sites-enabled/surfschool.conf \
 && mkdir -p /home/ana/nginx && chown ana: /home/ana/nginx \
 && systemctl enable nginx surf-api
STOPSIGNAL SIGRTMIN+3
CMD ["/sbin/init"]
