# P114's lab image: a stock Ubuntu 24.04 with systemd as PID 1, for every machine of a ski rental shop's small
# network: three web servers (web1, web2, web3) that serve the shop's page, and Ana's laptop (the control node,
# target "laptop": the same image plus Ubuntu's own ansible package). Ana is the first user on each (groups adm and
# sudo, as on a real install; sudo without a password, so Ansible's become needs no typed password).
FROM ubuntu:24.04 AS node
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends systemd systemd-sysv dbus sudo curl python3 \
      openssh-server openssh-client iproute2 procps less nano ca-certificates \
 && rm -f /usr/sbin/policy-rc.d \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash -G adm,sudo ana \
 && echo 'ana ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/ana && chmod 440 /etc/sudoers.d/ana \
 && touch /home/ana/.hushlogin \
 && systemctl enable ssh \
 && systemctl mask getty@tty1.service console-getty.service
STOPSIGNAL SIGRTMIN+3
CMD ["/sbin/init"]

FROM node AS laptop
RUN apt-get install -y --no-install-recommends ansible
COPY --chown=ana:ana ski /home/ana/ski
