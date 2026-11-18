# P148's machines: one stock Ubuntu 24.04 image for a pizza kitchen's order screen and its waiters' tablets.
# Ubuntu's own Python 3.12 runs the two small programs (kitchen.py, tablet.py); ss (iproute2) and tcpdump look at the
# sockets from outside. Ana is the first user (sudo without a password so the pty demo needs no typed password).
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends python3 iproute2 tcpdump ethtool iputils-ping \
      procps sudo less nano ca-certificates \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash -G sudo ana \
 && echo 'ana ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/ana && chmod 440 /etc/sudoers.d/ana \
 && touch /home/ana/.hushlogin
CMD ["sleep", "infinity"]
