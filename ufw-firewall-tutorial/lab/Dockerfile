# P174's lab: a tire shop's small network, every machine stock Ubuntu 24.04 with systemd as PID 1.
#   shop:     the shop's server. Ubuntu's openssh-server (Beth logs in from home), nginx serving the booking page
#             customers use (lab/shop/www), the bay screens page (lab/shop/bays.py, Ubuntu's Flask, port 5000) that
#             only the shop's own screens should see, Ubuntu's ufw (installed and inactive, as on a fresh Ubuntu
#             server) and Ubuntu's docker.io for the Docker chapter. Two network cards: the shop's own network
#             and the internet side.
#   home:     Beth's laptop at home, on the internet side: openssh-client, curl, netcat.
#   office:   Dave's PC in the shop office, on the shop's own network: curl, netcat.
#   phone:    a customer's phone on the internet side (a plain machine with curl).
#   stranger: an address on the internet side that keeps sending requests to the booking page.
FROM ubuntu:24.04
ARG ROLE=home
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends systemd systemd-sysv dbus sudo less nano procps \
      ca-certificates python3 iproute2 curl netcat-openbsd iputils-ping \
 && if [ "$ROLE" = shop ]; then apt-get install -y --no-install-recommends openssh-server nginx python3-flask ufw \
        rsyslog docker.io iptables tcpdump; \
    else apt-get install -y --no-install-recommends openssh-client; fi \
 && rm -f /usr/sbin/policy-rc.d \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash beth && useradd -m -s /bin/bash dave && useradd -m -s /bin/bash guest \
 && if [ "$ROLE" = shop ]; then usermod -aG sudo beth && echo 'beth ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/shop \
      && chmod 440 /etc/sudoers.d/shop; fi \
 && touch /home/beth/.hushlogin /home/dave/.hushlogin /home/guest/.hushlogin \
 && systemctl mask getty@tty1.service console-getty.service
COPY shop /srv/shop
RUN if [ "$ROLE" = shop ]; then cp /srv/shop/www/* /var/www/html/ && rm -f /var/www/html/index.nginx-debian.html \
      && sed -i 's/^worker_processes auto;/worker_processes 2;/' /etc/nginx/nginx.conf \
      && cp /srv/shop/bays.service /etc/systemd/system/ && systemctl enable bays.service ssh.service; fi
STOPSIGNAL SIGRTMIN+3
CMD ["/sbin/init"]
