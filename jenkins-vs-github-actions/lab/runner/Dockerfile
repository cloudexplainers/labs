# GitHub's own runner program (actions/runner 2.338.2) on a machine inside Ana's office network.
FROM ubuntu:24.04
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates gh git && rm -rf /var/lib/apt/lists/* \
 && useradd -m -s /bin/bash runner
WORKDIR /home/runner/actions-runner
RUN curl -fsSL https://github.com/actions/runner/releases/download/v2.338.2/actions-runner-linux-$(dpkg --print-architecture | sed s/amd64/x64/)-2.338.2.tar.gz | tar xz \
 && ./bin/installdependencies.sh && chown -R runner:runner /home/runner
