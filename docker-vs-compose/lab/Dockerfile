# Ana's laptop for P098: a stock Ubuntu 24.04 with systemd as PID 1, Ubuntu's own Docker (docker.io) and its
# Compose plugin (docker-compose-v2), so `docker` and `docker compose` work as on any Ubuntu laptop.
# demo.sh runs it --privileged with its own cgroup namespace and volumes for /var/lib/docker and /var/lib/containerd.
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends systemd systemd-sysv dbus sudo curl \
      iproute2 iptables procps ca-certificates docker.io docker-buildx docker-compose-v2 \
 && rm -f /usr/sbin/policy-rc.d \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash -G docker ana \
 && touch /home/ana/.hushlogin \
 && systemctl enable docker containerd \
 && systemctl mask getty@tty1.service console-getty.service
COPY shop /home/ana/shop
COPY stage /opt/stage
RUN chown -R ana:ana /home/ana/shop
STOPSIGNAL SIGRTMIN+3
CMD ["/sbin/init"]
