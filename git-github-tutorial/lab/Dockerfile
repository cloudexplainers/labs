# P166's lab: one image for both laptops (Ana's and Ben's, volunteers who keep a pottery class's website).
# Stock Ubuntu 24.04 with Ubuntu's own git and the GitHub CLI (gh), and python3 only to serve Ana's page to a browser.
# No global git settings: name, email and pull behaviour are set on camera, as on a fresh install.
FROM ubuntu:24.04
RUN apt-get update -qq && DEBIAN_FRONTEND=noninteractive apt-get install -y -qq --no-install-recommends \
      git gh ca-certificates python3 less >/dev/null \
 && rm -rf /var/lib/apt/lists/* && userdel -r ubuntu 2>/dev/null; \
    useradd -m -s /bin/bash ana && useradd -m -s /bin/bash ben
