# P170's lab: three machines at a small airfield, all stock Ubuntu 24.04 with systemd as PID 1.
#   laptop: Kari's laptop in the hangar office, Ubuntu's openssh-client, rsync and curl.
#   tower:  the server in the control tower, a fresh install with NO SSH server yet. Ubuntu's openssh-server packages
#           are downloaded into apt's cache when the image is built, so the install on camera is the real
#           `sudo apt install openssh-server`, just without the download wait. It runs the runway booking board,
#           a small page that listens on 127.0.0.1:8080 only (lab/board).
#   fuel:   the fuel depot's PC, with Ubuntu's openssh-server, on a second network only the tower can reach.
# Kari has an account everywhere (sudo without a typed password on the tower so the pty demo needs none); Tom has one
# on the tower. Their passwords are made-up lab passwords set by demo.sh; the lab is deleted after the run.
FROM ubuntu:24.04
ARG ROLE=laptop
ENV DEBIAN_FRONTEND=noninteractive
RUN rm -f /etc/apt/apt.conf.d/docker-clean \
 && apt-get update && apt-get install -y --no-install-recommends systemd systemd-sysv dbus sudo less nano procps \
      ca-certificates python3 iproute2 rsync curl tmux \
 && if [ "$ROLE" = tower ]; then apt-get install -y --download-only openssh-server && apt-get install -y --no-install-recommends ufw; \
    elif [ "$ROLE" = fuel ]; then apt-get install -y --no-install-recommends openssh-server; \
    else apt-get install -y --no-install-recommends openssh-client; fi \
 && rm -f /usr/sbin/policy-rc.d \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash kari && useradd -m -s /bin/bash tom \
 && if [ "$ROLE" = tower ]; then usermod -aG sudo kari && echo 'kari ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/airfield \
      && chmod 440 /etc/sudoers.d/airfield; fi \
 && touch /home/kari/.hushlogin /home/tom/.hushlogin \
 && systemctl mask getty@tty1.service console-getty.service
COPY board /srv/board
RUN if [ "$ROLE" = tower ]; then cp /srv/board/board.service /etc/systemd/system/ \
      && systemctl enable board.service; fi
STOPSIGNAL SIGRTMIN+3
CMD ["/sbin/init"]
