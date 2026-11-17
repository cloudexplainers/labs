# P119's machines: one stock Ubuntu 24.04 image with systemd as PID 1, standing in for a craft brewery's small
# network. Ubuntu's own Net-SNMP 5.9 packages: snmpd (the agent), snmptrapd (receives traps), snmp (the
# command-line tools snmpget/snmpwalk/snmptranslate) and the MIB files Ubuntu ships in libsnmp-base and
# snmp-mibs-downloader. Ana is the first user (sudo without a password so the pty demo needs no typed password).
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends systemd systemd-sysv dbus sudo snmp snmpd \
      snmptrapd snmp-mibs-downloader tcpdump iproute2 iputils-ping procps less nano curl python3 ca-certificates \
 && rm -f /usr/sbin/policy-rc.d \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash -G adm,sudo ana \
 && echo 'ana ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/ana && chmod 440 /etc/sudoers.d/ana \
 && touch /home/ana/.hushlogin \
 && systemctl mask getty@tty1.service console-getty.service
COPY wan-rate /usr/local/bin/wan-rate
STOPSIGNAL SIGRTMIN+3
CMD ["/sbin/init"]
