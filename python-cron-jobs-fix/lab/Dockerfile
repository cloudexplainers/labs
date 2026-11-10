# Ana's bike rental kiosk for P093: a stock Ubuntu 24.04 with systemd as PID 1 (so cron runs as the real service and
# journalctl shows its log), the cron package, Python 3 with venv support, and a user ana who may read the journal
# (group adm, as the first user on a real Ubuntu install). The shop's dashboard (lab/dashboard/app.py) runs as its
# own service on port 8000. Ana's project is copied in by the demo.
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends systemd systemd-sysv dbus sudo curl cron \
      procps python3 python3-venv less nano ca-certificates \
 && rm -f /usr/sbin/policy-rc.d \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash -G adm ana && useradd -r -s /usr/sbin/nologin dash \
 && systemctl mask getty@tty1.service console-getty.service
COPY dashboard/app.py /opt/dashboard/app.py
COPY dashboard/dashboard.service /etc/systemd/system/dashboard.service
RUN mkdir -p /var/lib/dashboard && chown dash /var/lib/dashboard && systemctl enable dashboard.service cron.service
STOPSIGNAL SIGRTMIN+3
CMD ["/sbin/init"]
