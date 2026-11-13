# The library's catalog server for P135: a stock Ubuntu 24.04 with systemd as PID 1, so apt's daily timers and
# unattended-upgrades are the real services. The image is the first 24.04 release (noble-20240423), so a fresh server
# really has security updates waiting, as a new cloud server does. libc6 is brought up to date at build time only
# because a libc6 upgrade restarts PID 1 and that stops a container. Docker's base image switches the daily apt jobs
# off (docker-disable-periodic-update); a real server has them on, so that file is removed. Two admins, ana and ben,
# have password-less sudo, as the default user on a cloud server does.
FROM ubuntu:noble-20240423
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends systemd systemd-sysv dbus sudo unattended-upgrades \
      procps psmisc lsof less ca-certificates libc6 libc-bin \
 && rm -f /usr/sbin/policy-rc.d /etc/apt/apt.conf.d/docker-clean /etc/apt/apt.conf.d/docker-disable-periodic-update \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash -G sudo ana && useradd -m -s /bin/bash -G sudo ben \
 && printf 'ana ALL=(ALL) NOPASSWD:ALL\nben ALL=(ALL) NOPASSWD:ALL\n' > /etc/sudoers.d/admins \
 && systemctl mask getty@tty1.service console-getty.service
STOPSIGNAL SIGRTMIN+3
CMD ["/sbin/init"]
