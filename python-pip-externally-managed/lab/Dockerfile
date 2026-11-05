# Ana's laptop for P072: a stock Ubuntu 24.04 with Python and pip from apt, the way a beginner gets them
# (sudo apt install python3-pip), plus software-properties-common, which every Ubuntu server ships.
# python3-venv and pipx are NOT installed: the demo installs them on camera.
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-pip sudo \
      software-properties-common ca-certificates \
 && rm -rf /var/lib/apt/lists/* \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash ana && echo 'ana:tea-for-two' | chpasswd && adduser ana sudo >/dev/null \
 && mkdir -p /home/ana/prices /srv/shop
COPY prices.py /home/ana/prices/prices.py
COPY prices.json /srv/shop/prices.json
RUN chown -R ana:ana /home/ana/prices
