# Ben's laptop for P097 "Every Django Concept a Beginner Needs to Know": a stock Ubuntu 24.04 with Python 3.12 and
# what a beginner installs first (python3-venv, curl), installed off camera. Django is installed from PyPI with pip
# inside a virtual environment during the run. socat forwards port 8001 to the development server on 127.0.0.1:8000,
# only so the browser captures can reach it from the host (off camera).
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-venv curl socat ca-certificates \
      procps \
 && rm -rf /var/lib/apt/lists/* \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash ben \
 && touch /home/ben/.hushlogin \
 && mkdir -p /home/ben/renovate && chown ben:ben /home/ben/renovate
COPY --chown=ben:ben steps /srv/steps
CMD ["socat", "TCP-LISTEN:8001,fork,reuseaddr", "TCP:127.0.0.1:8000"]
