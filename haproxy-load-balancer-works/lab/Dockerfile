# P113's machines: one stock Ubuntu 24.04 image with systemd as PID 1, standing in for a city marathon's sign-up
# site: the load balancer (Ubuntu's own HAProxy 2.8), three web servers (the sign-up app, Flask under gunicorn from
# Ubuntu's packages, as a systemd service) and a runner's laptop (curl, wrk). haproxy is installed on every box but
# only started on the load balancer; the sign-up service is only started on the web servers (demo.sh).
# Ana is the first user (sudo without a password so the pty demo needs no typed password).
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends systemd systemd-sysv dbus sudo python3 python3-flask \
      gunicorn haproxy curl wrk rsyslog iproute2 iputils-ping procps less ca-certificates \
 && rm -f /usr/sbin/policy-rc.d \
 && userdel -r ubuntu \
 && useradd -r -s /usr/sbin/nologin -d /var/lib/signup -m signup \
 && useradd -m -s /bin/bash -G adm,sudo,systemd-journal ana \
 && useradd -m -s /bin/bash ben \
 && echo 'ana ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/ana && chmod 440 /etc/sudoers.d/ana \
 && touch /home/ana/.hushlogin /home/ben/.hushlogin \
 && systemctl disable haproxy \
 && systemctl mask getty@tty1.service console-getty.service
COPY signup.py /opt/signup/signup.py
COPY signup.service /etc/systemd/system/signup.service
STOPSIGNAL SIGRTMIN+3
CMD ["/sbin/init"]
