# P169's lab: two machines at Linda's auto repair garage, both stock Ubuntu 24.04.
#   garage: the front office PC, systemd as PID 1, a fresh install with NO Redis yet. Ubuntu's redis-server packages
#           are downloaded into apt's cache when the image is built, so the install on camera is the real
#           `sudo apt install redis-server`, just without the download wait. python3-venv is there for the small
#           work-order script; its redis library is installed on camera with pip.
#   bay:    Rob's PC in the workshop bay, with only Ubuntu's redis-tools (redis-cli).
# Linda and Rob are users on the office PC (group sudo, sudo without a typed password so the pty demo needs none);
# Rob also has his own account on the bay PC. ~/.redisclirc turns off redis-cli's grey typing hints, which a pty
# recording would capture as noise.
FROM ubuntu:24.04
ARG ROLE=garage
ENV DEBIAN_FRONTEND=noninteractive
RUN rm -f /etc/apt/apt.conf.d/docker-clean \
 && apt-get update && apt-get install -y --no-install-recommends systemd systemd-sysv dbus sudo less nano procps \
      ca-certificates python3 python3-venv sqlite3 iproute2 \
 && if [ "$ROLE" = garage ]; then apt-get install -y --download-only redis-server; \
    else apt-get install -y --no-install-recommends redis-tools; fi \
 && rm -f /usr/sbin/policy-rc.d \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash -G sudo linda && useradd -m -s /bin/bash -G sudo rob \
 && printf 'linda ALL=(ALL) NOPASSWD:ALL\nrob ALL=(ALL) NOPASSWD:ALL\n' > /etc/sudoers.d/garage \
 && chmod 440 /etc/sudoers.d/garage \
 && touch /home/linda/.hushlogin /home/rob/.hushlogin \
 && for u in linda rob; do echo ':set nohints' > /home/$u/.redisclirc; chown $u:$u /home/$u/.redisclirc; done \
 && systemctl mask getty@tty1.service console-getty.service
COPY app /srv/app
STOPSIGNAL SIGRTMIN+3
CMD ["/sbin/init"]
