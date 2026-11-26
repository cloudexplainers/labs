# P176's lab: Jess's laptop. Stock Ubuntu 24.04 with Ubuntu's own git and no global Git settings beyond her name, so
# every message is what a fresh install prints. The railway's "server" is a bare repository on the same box
# (/srv/git/timetable.git), cloned into ~/timetable.
FROM ubuntu:24.04
RUN apt-get update -qq && DEBIAN_FRONTEND=noninteractive apt-get install -y -qq --no-install-recommends \
      git ca-certificates >/dev/null \
 && rm -rf /var/lib/apt/lists/* && userdel -r ubuntu 2>/dev/null; \
    useradd -m -s /bin/bash jess && useradd -m -s /bin/bash joe \
 && mkdir -p /srv/git && chmod 1777 /srv/git
