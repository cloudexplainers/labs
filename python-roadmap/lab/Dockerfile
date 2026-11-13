# Ana's laptop for P076 "The Python Roadmap for Beginners": a stock Ubuntu 24.04 with what a fresh Ubuntu desktop
# already has (python3) plus pip, venv, git and the "command not found" helper, installed off camera.
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-pip python3-venv git \
      command-not-found ca-certificates && apt-get update && update-command-not-found || true
RUN useradd -m -s /bin/bash ana && mkdir -p /home/ana/orders && mkdir -p /srv/v
COPY files/orders.csv files/hello.py /home/ana/orders/
COPY files/ /srv/v/
RUN chown -R ana:ana /home/ana && su ana -c 'git config --global user.name Ana && git config --global user.email ana@bakery.example && git config --global init.defaultBranch main'
CMD ["sleep", "infinity"]
