# P129's lab image: a stock Ubuntu 24.04 with systemd as PID 1, used for both machines of a bowling alley's small
# network: "lanes" (the server running the lane booking app, Ubuntu's own Flask, as a systemd service) and
# "front-desk" (the PC at the desk whose booking screen asks the server for free lanes). Ana is the first user
# (groups adm and sudo, as on a real install; sudo without a password so the pty demo needs no typed password).
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends systemd systemd-sysv dbus sudo curl python3 \
      python3-flask netcat-openbsd iputils-ping tcpdump iproute2 ufw openssh-client procps less nano ca-certificates \
 && rm -f /usr/sbin/policy-rc.d \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash -G adm,sudo ana \
 && echo 'ana ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/ana && chmod 440 /etc/sudoers.d/ana \
 && touch /home/ana/.hushlogin \
 && sed -i "s/^IPV6=yes/IPV6=no/" /etc/default/ufw \
 && systemctl mask getty@tty1.service console-getty.service
COPY lanes/app.py /srv/lanes/app.py
COPY lanes/lanes.service /etc/systemd/system/lanes.service
COPY lanes/book.py /home/ana/book.py
RUN chown -R ana:ana /srv/lanes /home/ana/book.py
STOPSIGNAL SIGRTMIN+3
CMD ["/sbin/init"]
