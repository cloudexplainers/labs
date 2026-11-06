# Ana's laptop for P091: Microsoft's Playwright image (Ubuntu 24.04, Python 3.12, Chromium already downloaded),
# plus a virtual environment with requests, Beautiful Soup, httpx and Playwright for Python.
FROM mcr.microsoft.com/playwright/python:v1.55.0-noble
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3-venv curl \
      && rm -rf /var/lib/apt/lists/* && useradd -m -s /bin/bash ana
USER ana
WORKDIR /home/ana/scraper
RUN python3 -m venv .venv && .venv/bin/pip install -q requests==2.32.5 beautifulsoup4==4.13.5 httpx==0.28.1 playwright==1.55.0
COPY --chown=ana:ana scraper/ /home/ana/scraper/
