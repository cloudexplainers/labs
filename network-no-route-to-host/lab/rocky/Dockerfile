# P173's tracker server: Rocky Linux 9 with systemd as PID 1 and firewalld on, as Rocky installs it. The railcar
# tracker app (tracker.py, Python's standard library only) runs as a systemd service on port 8080.
FROM rockylinux/rockylinux:9
RUN dnf -y install systemd firewalld python3 sudo procps-ng iproute tcpdump less && dnf clean all \
 && systemctl enable firewalld \
 && systemctl mask getty@tty1.service console-getty.service \
 && useradd -m -G wheel sarah \
 && echo 'sarah ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/sarah && chmod 440 /etc/sudoers.d/sarah \
 && touch /home/sarah/.hushlogin
COPY tracker.py /srv/tracker.py
COPY tracker.service /etc/systemd/system/tracker.service
RUN systemctl enable tracker
STOPSIGNAL SIGRTMIN+3
CMD ["/sbin/init"]
