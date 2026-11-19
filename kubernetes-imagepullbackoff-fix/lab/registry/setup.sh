#!/usr/bin/env bash
# Off camera, as root on Ana's laptop: the taco truck's private registry, registry.taco.lan.
# Our own lab CA signs its certificate; the registry (the official registry:3 image) asks for a user name and password
# (htpasswd) and joins kind's Docker network under the name registry.taco.lan, so the cluster's nodes reach it there.
# Ana's Docker and each node's containerd are told to trust our CA (the cluster's admin would do this once).
set -euo pipefail
cd /root
openssl req -x509 -newkey rsa:2048 -nodes -days 30 -subj "/CN=Taco truck lab CA" -keyout ca.key -out ca.crt 2>/dev/null
openssl req -newkey rsa:2048 -nodes -subj "/CN=registry.taco.lan" -keyout reg.key -out reg.csr 2>/dev/null
printf "subjectAltName=DNS:registry.taco.lan\n" > ext
openssl x509 -req -in reg.csr -CA ca.crt -CAkey ca.key -CAcreateserial -days 30 -extfile ext -out reg.crt 2>/dev/null
mkdir -p /srv/registry/certs /srv/registry/auth
cp reg.crt reg.key /srv/registry/certs/
htpasswd -Bbn ana "$1" > /srv/registry/auth/htpasswd
docker run -d -q --name registry --restart always --network kind --network-alias registry.taco.lan -p 443:443 \
  -e REGISTRY_HTTP_ADDR=0.0.0.0:443 -v /srv/registry/certs:/certs -v /srv/registry/auth:/auth \
  -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/reg.crt -e REGISTRY_HTTP_TLS_KEY=/certs/reg.key \
  -e REGISTRY_AUTH=htpasswd -e REGISTRY_AUTH_HTPASSWD_REALM=taco -e REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd \
  registry:3 >/dev/null
echo "127.0.0.1 registry.taco.lan" >> /etc/hosts
mkdir -p /etc/docker/certs.d/registry.taco.lan && cp ca.crt /etc/docker/certs.d/registry.taco.lan/
for n in taco-control-plane taco-worker taco-worker2; do
  d=/etc/containerd/certs.d/registry.taco.lan
  docker exec "$n" mkdir -p "$d"
  docker cp ca.crt "$n:$d/ca.crt"
  printf 'server = "https://registry.taco.lan"\n[host."https://registry.taco.lan"]\n  ca = "%s/ca.crt"\n' "$d" \
    | docker exec -i "$n" tee "$d/hosts.toml" >/dev/null
done
for i in $(seq 30); do
  [ "$(curl -s -o /dev/null -w '%{http_code}' --cacert ca.crt https://registry.taco.lan/v2/)" = 401 ] && exit 0
  sleep 1
done
echo "registry never answered" >&2; exit 1
