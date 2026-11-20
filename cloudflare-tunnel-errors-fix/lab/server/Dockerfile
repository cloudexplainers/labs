# Ana's homelab server for P143 "How to Fix Cloudflare Tunnel Errors in a Homelab": a stock Ubuntu 24.04 mini PC
# with systemd as PID 1 and Ubuntu's own Docker (docker.io) plus the Compose plugin. Ana is in the docker group.
# demo.sh runs it --privileged with its own cgroup namespace and fresh volumes for /var/lib/docker and
# /var/lib/containerd, so its Docker is its own; the club's site, its NAS and cloudflared run in it with Compose.
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends systemd systemd-sysv dbus sudo curl \
      iproute2 iptables procps ca-certificates openssl docker.io docker-compose-v2 \
 && rm -f /usr/sbin/policy-rc.d \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash -G sudo,docker ana && echo 'ana:lab-only-Meeple-club-7' | chpasswd \
 && touch /home/ana/.hushlogin \
 && systemctl enable docker containerd \
 && systemctl mask getty@tty1.service console-getty.service
# cloudflared itself too, from Cloudflare's own release (the same version as the container image), so Ana can check a
# named tunnel's config file with `cloudflared tunnel ingress validate` on the server.
ARG TARGETARCH
RUN curl -fsSL -o /tmp/cf.deb https://github.com/cloudflare/cloudflared/releases/download/2026.11.1/cloudflared-linux-${TARGETARCH}.deb \
 && dpkg -i /tmp/cf.deb && rm /tmp/cf.deb
STOPSIGNAL SIGRTMIN+3
CMD ["/sbin/init"]
