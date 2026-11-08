# Ana's laptop for P050: a stock Ubuntu 24.04 with curl, jq and Python (for ./doc). No key is baked in:
# demo.sh passes OPENROUTER_API_KEY at run time.
FROM ubuntu:24.04
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
      curl jq ca-certificates python3 && rm -rf /var/lib/apt/lists/*
RUN useradd -m -s /bin/bash ana
USER ana
COPY --chown=ana:ana shop /home/ana/shop
WORKDIR /home/ana/shop
