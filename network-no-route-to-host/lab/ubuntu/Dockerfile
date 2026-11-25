# P173's Ubuntu image: a stock Ubuntu 24.04 with systemd as PID 1, used for three machines of a freight yard's
# network: "yard-office" (Sarah's laptop), "yard-router" (the router between the office network and the scale
# house network) and "scale-house" (the weighbridge PC). Sarah is the first user (adm and sudo; sudo without a
# password so the pty demo needs no typed password).
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends systemd systemd-sysv dbus sudo curl python3 \
      netcat-openbsd iputils-ping tcpdump iproute2 procps less nano ca-certificates \
 && rm -f /usr/sbin/policy-rc.d \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash -G adm,sudo sarah \
 && echo 'sarah ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/sarah && chmod 440 /etc/sudoers.d/sarah \
 && touch /home/sarah/.hushlogin \
 && systemctl mask getty@tty1.service console-getty.service
COPY cars.py /home/sarah/cars.py
COPY weights.py /srv/weights.py
COPY weights.service /etc/systemd/system/weights.service
RUN chown sarah:sarah /home/sarah/cars.py
STOPSIGNAL SIGRTMIN+3
CMD ["/sbin/init"]
