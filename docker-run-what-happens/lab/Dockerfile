# Ana's laptop for P077: a stock Ubuntu 24.04 with systemd as PID 1 and Ubuntu's own Docker (docker.io), so
# dockerd, containerd and runc run as they do on any Linux laptop. A sudo user ana in the docker group.
# demo.sh runs it --privileged (Docker inside needs to make namespaces, cgroups and mounts) with its own cgroup
# namespace and a volume for /var/lib/docker; nginx is NOT pulled: the demo pulls it on camera.
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends systemd systemd-sysv dbus sudo curl jq \
      iproute2 iptables psmisc procps ca-certificates docker.io \
 && rm -f /usr/sbin/policy-rc.d \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash -G sudo,docker ana && echo 'ana:lab-only-Kettle-laptop-7' | chpasswd \
 && touch /home/ana/.hushlogin \
 && systemctl enable docker containerd \
 && systemctl mask getty@tty1.service console-getty.service
STOPSIGNAL SIGRTMIN+3
CMD ["/sbin/init"]
