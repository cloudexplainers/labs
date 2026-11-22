# P168's machines: stock Ubuntu 24.04 with Ubuntu's own Python 3.12, curl, jq and less.
# office: the car lot's office PC, where Linda builds the MCP server (uv is NOT installed: she installs it on camera).
# sales: the sales desk PC Rob uses, with Node.js (copied from the official node image) for the MCP Inspector, to reach the
#         office PC's server over the network.
FROM node:24-bookworm-slim AS node

FROM ubuntu:24.04 AS office
ENV DEBIAN_FRONTEND=noninteractive NPM_CONFIG_UPDATE_NOTIFIER=false NPM_CONFIG_FUND=false
RUN apt-get update && apt-get install -y --no-install-recommends python3 curl ca-certificates jq less procps \
      iproute2 \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash linda \
 && touch /home/linda/.hushlogin
COPY --from=node /usr/local/bin/node /usr/local/bin/node
COPY --from=node /usr/local/lib/node_modules /usr/local/lib/node_modules
RUN ln -s ../lib/node_modules/npm/bin/npm-cli.js /usr/local/bin/npm \
 && ln -s ../lib/node_modules/npm/bin/npx-cli.js /usr/local/bin/npx
# the MCP Inspector installed ahead, so `npx @modelcontextprotocol/inspector` starts without a download on camera
RUN npm install -g @modelcontextprotocol/inspector@2.16.0 >/dev/null \
 && printf "update-notifier=false\nfund=false\n" > /usr/local/etc/npmrc
CMD ["sleep", "infinity"]

FROM office AS sales
RUN userdel -r linda && useradd -m -s /bin/bash rob && touch /home/rob/.hushlogin
