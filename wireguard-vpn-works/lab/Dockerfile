# One image for every machine in P105's lab: a stock Ubuntu 24.04 with the archive's WireGuard tools (the WireGuard
# code itself is in the Linux kernel), the usual network tools, and two users who may use sudo, as the first
# user on a real Ubuntu install can: ana (the print shop's machines) and sam (the stranger's). The demo starts six containers from it: laptop, hotel-wifi, hotspot, gateway, files and
# stranger (demo.sh).
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends wireguard-tools iproute2 iptables tcpdump curl \
      iputils-ping netcat-openbsd python3 sudo less nano ca-certificates procps \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash -G sudo ana && useradd -m -s /bin/bash -G sudo sam \
 && echo '%sudo ALL=(ALL) NOPASSWD: ALL' > /etc/sudoers.d/ana \
 && echo 'Defaults !admin_flag' >> /etc/sudoers.d/ana && touch /home/ana/.sudo_as_admin_successful /home/sam/.sudo_as_admin_successful
CMD ["sleep", "infinity"]
