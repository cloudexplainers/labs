# P130's lab: one stock Ubuntu 24.04 image for both boxes. The club's laptop (Ana, a fresh user with no ~/.ssh) and git-server,
# our own Git server set up the way GitHub's SSH side works: every account connects as the user "git", keys only
# (no passwords; its shell only ever runs gitserve, which hands git commands to git-shell), and the key you offer decides who you are (authorized_keys runs gitserve with your name).
FROM ubuntu:24.04
RUN apt-get update -qq && DEBIAN_FRONTEND=noninteractive apt-get install -y -qq --no-install-recommends \
      git openssh-client openssh-server sudo ca-certificates >/dev/null \
 && rm -rf /var/lib/apt/lists/* && userdel -r ubuntu 2>/dev/null; \
    useradd -m -s /bin/sh git && useradd -m -s /bin/bash -G sudo ana \
 && echo 'ana:sailing' | chpasswd
COPY sshd_config /etc/ssh/sshd_config.d/10-keys-only.conf
COPY gitserve /usr/local/bin/gitserve
RUN chmod 755 /usr/local/bin/gitserve
