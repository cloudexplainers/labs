# The ferry office's Linux box for P117 "Linux Makefiles Will Finally Make Sense After This": a stock Ubuntu 24.04
# with GNU make and the C compiler from Ubuntu's archive. Ana's small C program waits in /srv/src, and each version
# of her Makefile in /srv/mk; the demo copies them into her project folder off camera, one file at a time, like a
# file saved from an editor. Lua's real source (MIT licence, lua.org) waits in /srv/lua and is copied to ~/lua for the timing chapter.
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends make gcc libc6-dev curl ca-certificates \
 && rm -rf /var/lib/apt/lists/* \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash ana
ARG LUA=5.4.8
RUN curl -fsSL --retry 6 --retry-all-errors https://www.lua.org/ftp/lua-$LUA.tar.gz | tar xz -C /srv \
 && mv /srv/lua-$LUA /srv/lua && chown -R ana:ana /srv/lua
COPY --chown=ana:ana src /srv/src
COPY --chown=ana:ana mk /srv/mk
CMD ["sleep", "infinity"]
