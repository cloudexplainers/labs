#!/bin/sh
# The lab's own certificate authority, made like a real one: a root that signs one intermediate ("issuing")
# CA, which signs the shop's certificate. The certificate names where to download its issuer (caIssuers), as
# real ones do. Files land where certbot puts them: cert.pem, chain.pem, fullchain.pem, privkey.pem.
set -eu
D=/root/ca; mkdir -p $D /etc/ssl/shop; cd $D
ec() { openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-256 -out "$1" 2>/dev/null; }
ec root.key; ec issuing.key; ec /etc/ssl/shop/privkey.pem
openssl req -x509 -new -key root.key -days 3650 -subj "/CN=Kettle Lab Root CA" \
  -addext "basicConstraints=critical,CA:TRUE" -addext "keyUsage=critical,keyCertSign,cRLSign" -out root.pem
openssl req -new -key issuing.key -subj "/CN=Kettle Lab Issuing CA" -out issuing.csr
printf 'basicConstraints=critical,CA:TRUE,pathlen:0\nkeyUsage=critical,keyCertSign,cRLSign\nsubjectKeyIdentifier=hash\nauthorityKeyIdentifier=keyid\n' > issuing.ext
openssl x509 -req -in issuing.csr -CA root.pem -CAkey root.key -CAcreateserial -days 1825 -extfile issuing.ext \
  -out issuing.pem 2>/dev/null
openssl req -new -key /etc/ssl/shop/privkey.pem -subj "/CN=shop.test" -out shop.csr
printf 'subjectAltName=DNS:shop.test\nbasicConstraints=critical,CA:FALSE\nkeyUsage=critical,digitalSignature\nextendedKeyUsage=serverAuth\nauthorityInfoAccess=caIssuers;URI:http://ca.test/issuing-ca.crt\nsubjectKeyIdentifier=hash\nauthorityKeyIdentifier=keyid\n' > shop.ext
openssl x509 -req -in shop.csr -CA issuing.pem -CAkey issuing.key -CAcreateserial -days 90 -extfile shop.ext \
  -out /etc/ssl/shop/cert.pem 2>/dev/null
cp issuing.pem /etc/ssl/shop/chain.pem
cat /etc/ssl/shop/cert.pem /etc/ssl/shop/chain.pem > /etc/ssl/shop/fullchain.pem
openssl x509 -in issuing.pem -outform der -out /var/www/ca/issuing-ca.crt
chmod 600 /etc/ssl/shop/privkey.pem
cp root.pem /usr/local/share/ca-certificates/kettle-lab-root.crt && update-ca-certificates >/dev/null 2>&1
