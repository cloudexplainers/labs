FROM ubuntu:24.04
RUN apt-get update && apt-get install -y --no-install-recommends git gh ca-certificates curl python3 python3-pytest less && rm -rf /var/lib/apt/lists/* \
 && useradd -m -s /bin/bash ana
