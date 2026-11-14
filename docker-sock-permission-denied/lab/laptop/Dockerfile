# The music school's office PC for P137: a stock Ubuntu 24.04 with systemd as PID 1 and Ubuntu's own Docker
# (docker.io). Ana set it up and is in the docker group; Ben is new: a sudo user, not in the docker group;
# Cara is a part-time account with no sudo and no docker. demo.sh runs it --privileged with its own cgroup
# namespace and a fresh volume for /var/lib/docker, so its Docker starts empty; the images are loaded off-screen.
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends systemd systemd-sysv dbus sudo curl \
      iproute2 iptables procps ca-certificates docker.io \
 && rm -f /usr/sbin/policy-rc.d \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash -G sudo,docker ana && echo 'ana:lab-only-Piano-office-4' | chpasswd \
 && useradd -m -s /bin/bash -G sudo ben && echo 'ben:lab-only-Cello-office-7' | chpasswd \
 && useradd -m -s /bin/bash cara && echo 'cara:lab-only-Flute-office-2' | chpasswd \
 && touch /home/ana/.hushlogin /home/ben/.hushlogin /home/cara/.hushlogin \
 && systemctl enable docker containerd \
 && systemctl mask getty@tty1.service console-getty.service
STOPSIGNAL SIGRTMIN+3
CMD ["/sbin/init"]
