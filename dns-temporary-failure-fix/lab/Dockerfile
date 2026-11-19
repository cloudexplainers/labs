# P138's lab image: a stock Ubuntu 24.04 with systemd as PID 1 and Ubuntu's own systemd-resolved, as on an installed
# server, for a bike courier depot's small network.
#   target "pc":     dispatch, the depot's Ubuntu server (it plans the riders' routes and downloads its updates):
#                    systemd-resolved with its stub on 127.0.0.53, netplan + systemd-networkd, dig, curl, ufw.
#   target "router": the depot's router, whose dnsmasq answers DNS for the depot and forwards the rest.
# Ana is the first user (groups adm and sudo, sudo without a password so the pty demo needs no typed password).
FROM ubuntu:24.04 AS base
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends systemd systemd-sysv dbus sudo curl iproute2 \
      iputils-ping procps less nano ca-certificates bind9-dnsutils \
 && rm -f /usr/sbin/policy-rc.d \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash -G adm,sudo ana \
 && echo 'ana ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/ana && chmod 440 /etc/sudoers.d/ana \
 && touch /home/ana/.hushlogin \
 && systemctl mask getty@tty1.service console-getty.service
STOPSIGNAL SIGRTMIN+3
CMD ["/sbin/init"]

FROM base AS pc
RUN apt-get update && apt-get install -y --no-install-recommends systemd-resolved netplan.io ufw \
 && sed -i "s/^IPV6=yes/IPV6=no/" /etc/default/ufw
COPY pc/50-depot.yaml /etc/netplan/50-depot.yaml
COPY pc/resolv-link.service /etc/systemd/system/resolv-link.service
RUN chmod 600 /etc/netplan/50-depot.yaml && systemctl enable resolv-link.service systemd-networkd && netplan generate

FROM base AS router
RUN apt-get update && apt-get install -y --no-install-recommends dnsmasq
COPY router/depot.conf /etc/dnsmasq.d/depot.conf
