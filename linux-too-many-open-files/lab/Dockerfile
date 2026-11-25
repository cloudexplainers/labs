# P172's lab image: a stock Ubuntu 24.04 with systemd as PID 1, the laundromat's payment server. The payment app
# (washpay.py, Python's standard library only) runs as a systemd service; Jim is the first user (adm and sudo;
# sudo without a password so the pty demo needs no typed password). demo.sh starts it with Ubuntu's usual limit
# for a login (1024 open files, hard 524288) instead of Docker's much higher default.
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends systemd systemd-sysv dbus sudo curl python3 \
      lsof procps iproute2 less nano ca-certificates \
 && rm -f /usr/sbin/policy-rc.d \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash -G adm,sudo jim \
 && echo 'jim ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/jim && chmod 440 /etc/sudoers.d/jim \
 && touch /home/jim/.hushlogin \
 && useradd -r -s /usr/sbin/nologin washpay && mkdir -p /var/log/washpay && chown washpay /var/log/washpay \
 && systemctl mask getty@tty1.service console-getty.service
COPY washpay.py /srv/washpay/washpay.py
COPY washpay.service /etc/systemd/system/washpay.service
COPY pay.sh /home/jim/pay.sh
RUN chmod +x /home/jim/pay.sh && chown jim:jim /home/jim/pay.sh && systemctl enable washpay
STOPSIGNAL SIGRTMIN+3
CMD ["/sbin/init"]
