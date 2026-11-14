# One image for every machine in P147's lab: a stock Ubuntu 24.04 with the network tools from Ubuntu's archive.
FROM ubuntu:24.04
RUN apt-get update -qq && DEBIAN_FRONTEND=noninteractive apt-get install -y -qq --no-install-recommends \
      sudo iproute2 iputils-ping iputils-tracepath dnsutils curl tcpdump iptables nftables netcat-openbsd \
      dnsmasq isc-dhcp-client python3 procps ethtool >/dev/null \
 && rm -rf /var/lib/apt/lists/* \
 && (userdel -r ubuntu 2>/dev/null || true) \
 && useradd -m -s /bin/bash ana && useradd -m -s /bin/bash ben \
 && printf 'ana ALL=(ALL) NOPASSWD:ALL\nben ALL=(ALL) NOPASSWD:ALL\n' > /etc/sudoers.d/lab
