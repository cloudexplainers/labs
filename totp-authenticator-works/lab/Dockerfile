# P111's machines: one stock Ubuntu 24.04 image with systemd as PID 1, standing in for a scuba dive shop's booking
# server, Ana's laptop and Ana's phone. Ubuntu's own packages: Flask and pyotp (the shop's login), oathtool (the
# phone's codes), qrencode and zbar-tools (the setup QR code), faketime (a phone clock set wrong), curl, jq.
# Ana is the first user (sudo without a password so the pty demo needs no typed password).
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends systemd systemd-sysv dbus sudo python3 python3-flask \
      python3-pyotp oathtool qrencode zbar-tools faketime curl jq iproute2 iputils-ping procps less ca-certificates \
 && rm -f /usr/sbin/policy-rc.d \
 && userdel -r ubuntu \
 && useradd -r -s /usr/sbin/nologin diveshop \
 && useradd -m -s /bin/bash -G adm,sudo ana \
 && echo 'ana ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/ana && chmod 440 /etc/sudoers.d/ana \
 && touch /home/ana/.hushlogin \
 && systemctl mask getty@tty1.service console-getty.service
COPY diveshop.py /opt/diveshop/diveshop.py
COPY diveshop.service /etc/systemd/system/diveshop.service
COPY authenticator totp-steps /usr/local/bin/
RUN chmod 755 /usr/local/bin/authenticator /usr/local/bin/totp-steps
STOPSIGNAL SIGRTMIN+3
CMD ["/sbin/init"]
