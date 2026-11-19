# P139's lab image: a stock Ubuntu 24.04 with systemd as PID 1 and the real cron, as a small theatre's box-office
# server ("boxoffice"). The AWS CLI v2 is installed from AWS's own installer (pinned below), as AWS's docs describe.
# Ana is the first user (groups adm and sudo, as on a real install; sudo without a password so the pty demo needs no
# typed password).
FROM ubuntu:24.04
ARG TARGETARCH
ARG AWSCLI=2.41.1
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends systemd systemd-sysv dbus sudo curl unzip cron \
      iproute2 procps less nano ca-certificates groff-base \
 && rm -f /usr/sbin/policy-rc.d \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash -G adm,sudo ana \
 && echo 'ana ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/ana && chmod 440 /etc/sudoers.d/ana \
 && touch /home/ana/.hushlogin \
 && systemctl mask getty@tty1.service console-getty.service \
 && systemctl enable cron
RUN arch=$([ "$TARGETARCH" = arm64 ] && echo aarch64 || echo x86_64) \
 && curl -fsSLo /tmp/awscliv2.zip "https://awscli.amazonaws.com/awscli-exe-linux-${arch}-${AWSCLI}.zip" \
 && cd /tmp && unzip -q awscliv2.zip && ./aws/install && rm -rf /tmp/aws /tmp/awscliv2.zip
STOPSIGNAL SIGRTMIN+3
CMD ["/sbin/init"]
