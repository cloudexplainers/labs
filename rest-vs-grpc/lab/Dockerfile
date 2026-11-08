# One image for both machines in P112 "REST vs gRPC": a stock Ubuntu 24.04 with Python 3.12 from apt, one virtual
# environment (~/.venv) with FastAPI, Uvicorn, httpx, grpcio and grpcio-tools from PyPI, curl, and grpcurl (the
# command-line gRPC client, from its GitHub release). The stock machine runs Ana's stock service (lab/stock/);
# the laptop holds her order service's small client scripts (lab/laptop/).
FROM ubuntu:24.04
ARG TARGETARCH
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-venv curl ca-certificates procps \
 && rm -rf /var/lib/apt/lists/* \
 && arch=$([ "$TARGETARCH" = arm64 ] && echo arm64 || echo x86_64) \
 && curl -sSL "https://github.com/fullstorydev/grpcurl/releases/download/v1.9.4/grpcurl_1.9.4_linux_${arch}.tar.gz" \
    | tar -xz -C /usr/local/bin grpcurl \
 && userdel -r ubuntu && useradd -m -s /bin/bash ana
USER ana
RUN python3 -m venv /home/ana/.venv \
 && /home/ana/.venv/bin/pip install --no-cache-dir -q fastapi uvicorn httpx grpcio grpcio-tools
ENV PATH=/home/ana/.venv/bin:$PATH VIRTUAL_ENV=/home/ana/.venv
COPY --chown=ana:ana stock/ /home/ana/stock-service/
COPY --chown=ana:ana laptop/ /home/ana/order-service/
CMD ["sleep", "infinity"]
