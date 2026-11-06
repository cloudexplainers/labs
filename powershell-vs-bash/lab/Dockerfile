# Ana's laptop for "PowerShell vs Bash": a stock Ubuntu 24.04 with bash (it comes with the image) and
# PowerShell 7, installed from Microsoft's own package repository, plus curl, jq and Python for the orders page.
FROM ubuntu:24.04
RUN apt-get update && apt-get install -y --no-install-recommends wget ca-certificates curl jq python3 \
 && wget -q https://packages.microsoft.com/config/ubuntu/24.04/packages-microsoft-prod.deb \
 && dpkg -i packages-microsoft-prod.deb && rm packages-microsoft-prod.deb \
 && apt-get update && apt-get install -y --no-install-recommends powershell && rm -rf /var/lib/apt/lists/* \
 && useradd -m -s /bin/bash ana
COPY --chown=ana:ana shop /home/ana/shop
COPY --chown=ana:ana make_logs.sh /home/ana/make_logs.sh
USER ana
WORKDIR /home/ana/shop
RUN sh /home/ana/make_logs.sh && rm /home/ana/make_logs.sh
CMD ["python3", "-m", "http.server", "8080", "--bind", "127.0.0.1", "--directory", "/home/ana/shop/web"]
