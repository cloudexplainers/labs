# Ana's laptop for P099: a stock Ubuntu 24.04 with systemd as PID 1 and Ubuntu's own Docker and Compose
# (docker.io, docker-compose-v2), plus the PostgreSQL client. A sudo user ana in the docker group.
# demo.sh runs it --privileged with its own cgroup namespace and fresh volumes for /var/lib/docker and
# /var/lib/containerd (P077), so its Docker starts empty; the two images the shop uses are loaded off-screen.
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends systemd systemd-sysv dbus sudo curl jq \
      iproute2 iptables procps ca-certificates docker.io docker-compose-v2 postgresql-client \
 && rm -f /usr/sbin/policy-rc.d \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash -G sudo,docker ana && echo 'ana:lab-only-Kettle-laptop-9' | chpasswd \
 && touch /home/ana/.hushlogin \
 && systemctl enable docker containerd \
 && systemctl mask getty@tty1.service console-getty.service
STOPSIGNAL SIGRTMIN+3
CMD ["/sbin/init"]
