# P136's office PC: a stock Ubuntu 24.04 with systemd as PID 1, the PostgreSQL client, Python with psycopg2 for the
# school's booking script, and Ubuntu's own Docker and Compose for a test copy of the database. demo.sh runs it
# --privileged with its own cgroup namespace and fresh volumes, so its Docker starts empty (P077, P099); the
# postgres image is loaded off-screen. Ana is a sudo user in the docker group.
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends systemd systemd-sysv dbus sudo curl \
      iproute2 iptables procps less nano ca-certificates docker.io docker-compose-v2 postgresql-client \
      python3 python3-psycopg2 \
 && rm -f /usr/sbin/policy-rc.d \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash -G sudo,docker ana \
 && echo 'ana ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/ana && chmod 440 /etc/sudoers.d/ana \
 && touch /home/ana/.hushlogin \
 && systemctl enable docker containerd \
 && systemctl mask getty@tty1.service console-getty.service
COPY school /home/ana/school
COPY testdb /home/ana/testdb
RUN chown -R ana:ana /home/ana/school /home/ana/testdb
STOPSIGNAL SIGRTMIN+3
CMD ["/sbin/init"]
