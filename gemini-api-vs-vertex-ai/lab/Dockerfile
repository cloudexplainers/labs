# Ana's laptop for P048: a stock Ubuntu 24.04 with curl, jq and Python, plus Google's official Gen AI SDK
# (google-genai) in a virtual environment. No key or credential is baked in: demo.sh passes them at run time.
FROM ubuntu:24.04
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
      curl jq ca-certificates python3 python3-venv && rm -rf /var/lib/apt/lists/*
RUN useradd -m -s /bin/bash ana
USER ana
RUN python3 -m venv /home/ana/.venv && /home/ana/.venv/bin/pip install -q google-genai==3.0.0
ENV PATH=/home/ana/.venv/bin:$PATH
COPY --chown=ana:ana shop /home/ana/shop
WORKDIR /home/ana/shop
