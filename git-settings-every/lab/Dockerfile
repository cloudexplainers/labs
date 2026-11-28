# P181's lab: Linda's new laptop. Stock Ubuntu 24.04 with Ubuntu's own git and nano, and no Git settings at all, so
# every message is what a fresh install prints. Rob's laptop is a second user on the same box, already set up. The
# household's shared repository is a bare repository on the same box (/srv/git/chores.git).
FROM ubuntu:24.04
RUN apt-get update -qq && DEBIAN_FRONTEND=noninteractive apt-get install -y -qq --no-install-recommends \
      git nano ca-certificates >/dev/null \
 && rm -rf /var/lib/apt/lists/* && userdel -r ubuntu 2>/dev/null; \
    useradd -m -s /bin/bash -c "Linda" linda && useradd -m -s /bin/bash -c "Rob" rob \
 && mkdir -p /srv/git && chmod 1777 /srv/git
