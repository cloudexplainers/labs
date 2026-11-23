# P125's database server, "dispatch-db": a stock Ubuntu 24.04 with systemd as PID 1 and Ubuntu's own MySQL server
# (mysql-server from the Ubuntu archive), standing in for a plumbing company's office server. mysqld listens on every
# address (Ubuntu's default is 127.0.0.1 only), so the dispatch board PC on the office network can reach it, and
# skip-name-resolve makes it name clients by address (as MySQL's docs suggest when hosts have no DNS names).
# The mysql client's prompt carries a marker the demo driver waits for (shown as "mysql> " on screen).
# Trish is the first user (groups adm and sudo; sudo without a password so the pty demo needs no typed password).
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends systemd systemd-sysv dbus sudo mysql-server \
      iproute2 procps less nano ca-certificates \
 && rm -f /usr/sbin/policy-rc.d \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash -G adm,sudo trish \
 && echo 'trish ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/trish && chmod 440 /etc/sudoers.d/trish \
 && touch /home/trish/.hushlogin \
 && printf '[mysqld]\nbind-address = 0.0.0.0\nskip-name-resolve\n' > /etc/mysql/mysql.conf.d/zz-office.cnf \
 && printf '[mysql]\nprompt=__REA''DY__:mysql:__\\_\n' > /etc/mysql/conf.d/zz-demo-prompt.cnf \
 && systemctl mask getty@tty1.service console-getty.service
STOPSIGNAL SIGRTMIN+3
CMD ["/sbin/init"]
