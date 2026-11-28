# P180's lab machines, all stock Ubuntu 24.04 with systemd as PID 1 (demo.sh builds one image per ROLE).
#   basement:   the apartment building's server in the basement: the laundry booking page (lab/booking) on :8080
#               and SSH; Tailscale is installed on camera with Tailscale's own install script.
#   laptop:     John's laptop at a cafe; Tailscale installed on camera too.
#   jen-laptop: Jen's laptop at her office (a tenant); Tailscale installed off camera with the same script.
#   doorcam:    the front-door camera's recorder on the building network, which can't run Tailscale (lab/doorcam).
#   headscale:  the lab's coordination server: Headscale, the open-source server the Tailscale app can log in to,
#               from its own release .deb (lab/headscale/config.yaml), so no Tailscale account is needed.
#   whoami:     a small website on "the internet" that prints the address a visitor comes from (lab/whoami).
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends systemd systemd-sysv dbus sudo less procps \
      ca-certificates curl python3 iproute2 iputils-ping openssh-server openssh-client nano netcat-openbsd \
 && rm -rf /var/lib/apt/lists/* /usr/sbin/policy-rc.d \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash -G sudo john && useradd -m -s /bin/bash -G sudo jen \
 && echo 'john ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/lab && echo 'jen ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers.d/lab \
 && chmod 440 /etc/sudoers.d/lab && touch /home/john/.hushlogin /home/jen/.hushlogin \
 && systemctl mask getty@tty1.service console-getty.service systemd-resolved.service
ARG ROLE=basement
ARG HEADSCALE=0.29.8
RUN if [ "$ROLE" = headscale ]; then curl -fsSL -o /tmp/hs.deb \
      "https://github.com/juanfont/headscale/releases/download/v${HEADSCALE}/headscale_${HEADSCALE}_linux_amd64.deb" \
      && apt-get install -y /tmp/hs.deb && rm /tmp/hs.deb; fi
COPY booking /srv/booking
COPY doorcam /srv/doorcam
COPY whoami /srv/whoami
COPY headscale/config.yaml /srv/headscale-config.yaml
RUN case "$ROLE" in \
      basement) cp /srv/booking/booking.service /etc/systemd/system/ && systemctl enable booking.service ;; \
      doorcam) cp /srv/doorcam/doorcam.service /etc/systemd/system/ && systemctl enable doorcam.service ;; \
      whoami) cp /srv/whoami/whoami.service /etc/systemd/system/ && systemctl enable whoami.service ;; \
      headscale) cp /srv/headscale-config.yaml /etc/headscale/config.yaml && systemctl enable headscale.service ;; \
    esac
STOPSIGNAL SIGRTMIN+3
CMD ["/sbin/init"]
