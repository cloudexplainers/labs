# Ana's laptop for P164 "Docker: Full Tutorial for Beginners": a stock Ubuntu 24.04 with systemd as PID 1 and
# Ubuntu's own Docker (docker.io) plus the Compose plugin (docker-compose-v2). Ana is in the docker group, as after
# the post-install step. demo.sh runs it --privileged with its own cgroup namespace and fresh volumes for
# /var/lib/docker and /var/lib/containerd, so its Docker starts empty: every image is pulled from Docker Hub on camera.
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends systemd systemd-sysv dbus sudo curl \
      iproute2 iptables procps ca-certificates docker.io docker-compose-v2 docker-buildx \
 && rm -f /usr/sbin/policy-rc.d \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash -G sudo,docker ana && echo 'ana:lab-only-Willow-yoga-5' | chpasswd \
 && touch /home/ana/.hushlogin \
 && systemctl enable docker containerd \
 && systemctl mask getty@tty1.service console-getty.service
STOPSIGNAL SIGRTMIN+3
CMD ["/sbin/init"]
