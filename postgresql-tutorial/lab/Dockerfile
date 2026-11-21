# P167's lab: the office PC at Pine Hollow, a small campground. A stock Ubuntu 24.04 with systemd as PID 1, as a
# fresh install: PostgreSQL is NOT installed. Its packages are downloaded into apt's cache when the image is built
# (so the install on camera is the real `apt install postgresql`, just without the download wait), and Ubuntu's
# python3-psycopg2 is installed for the small booking script. Ana and Ben are the two people at the front desk
# (groups sudo; sudo without a password so the pty demo needs no typed password).
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN rm -f /etc/apt/apt.conf.d/docker-clean \
 && apt-get update && apt-get install -y --no-install-recommends systemd systemd-sysv dbus sudo less nano \
      ca-certificates python3 python3-psycopg2 locales \
 && apt-get install -y --download-only postgresql \
 && rm -f /usr/sbin/policy-rc.d \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash -G sudo ana && useradd -m -s /bin/bash -G sudo ben \
 && printf 'ana ALL=(ALL) NOPASSWD:ALL\nben ALL=(ALL) NOPASSWD:ALL\n' > /etc/sudoers.d/desk && chmod 440 /etc/sudoers.d/desk \
 && touch /home/ana/.hushlogin /home/ben/.hushlogin \
 && systemctl mask getty@tty1.service console-getty.service
STOPSIGNAL SIGRTMIN+3
CMD ["/sbin/init"]
