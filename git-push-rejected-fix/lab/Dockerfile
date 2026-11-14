# P134's lab: one image for all three boxes. A Git server standing in for GitHub (SSH, user git with git-shell, bare
# repositories) and two laptops, Ana's and Ben's. Stock Ubuntu 24.04 with Ubuntu's own git, no global pull settings,
# so git pull behaves as it does on a fresh install.
FROM ubuntu:24.04
RUN apt-get update -qq && DEBIAN_FRONTEND=noninteractive apt-get install -y -qq --no-install-recommends \
      git openssh-client openssh-server ca-certificates >/dev/null \
 && rm -rf /var/lib/apt/lists/* && userdel -r ubuntu 2>/dev/null; \
    useradd -m -s /usr/bin/git-shell git && useradd -m -s /bin/bash ana && useradd -m -s /bin/bash ben
