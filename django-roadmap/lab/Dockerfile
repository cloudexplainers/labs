# Dave's laptop for P096 "The Django Roadmap for Beginners": a stock Ubuntu 24.04 with Python 3.12 and what a
# beginner installs first (python3-venv for virtual environments, curl), installed off camera. Django itself is
# installed on camera from PyPI with pip inside a virtual environment. socat forwards port 8001 to the development
# server on 127.0.0.1:8000, only so the browser captures can reach it from the host (off camera).
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-venv curl socat ca-certificates \
      procps \
 && rm -rf /var/lib/apt/lists/* \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash dave \
 && touch /home/dave/.hushlogin \
 && mkdir -p /home/dave/potluck && chown dave:dave /home/dave/potluck
COPY --chown=dave:dave steps /srv/steps
CMD ["socat", "TCP-LISTEN:8001,fork,reuseaddr", "TCP:127.0.0.1:8000"]
