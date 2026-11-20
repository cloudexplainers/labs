# A friend's laptop on the internet for P143: a stock Ubuntu 24.04 with curl. It reaches the club's site only
# through its public trycloudflare.com address, like any visitor.
FROM ubuntu:24.04
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates \
 && useradd -m -s /bin/bash ben && touch /home/ben/.hushlogin
CMD ["sleep", "infinity"]
