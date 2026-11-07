# Ana's laptop for P090: a stock Ubuntu 24.04 with Python, pip and venv from apt, the way a beginner gets them
# (sudo apt install python3-pip python3-venv), plus curl for uv's installer. uv itself is installed on camera.
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-pip python3-venv curl \
      ca-certificates \
 && rm -rf /var/lib/apt/lists/* \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash ana \
 && mkdir -p /home/ana/shop /srv/shop
COPY requirements.txt app.py /home/ana/shop/
COPY prices.json /srv/shop/prices.json
RUN chown -R ana:ana /home/ana/shop
