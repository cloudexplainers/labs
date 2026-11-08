# How to Fix SSL Certificate Chain Errors (Missing Intermediate)

Video: https://youtu.be/ZjkJv_WmRqw  
Written version: https://cloudexplainers.com/how-to-fix-ssl-certificate-chain-errors-missing-intermediate/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile.laptop`](lab/Dockerfile.laptop)
- [`lab/Dockerfile.shop`](lab/Dockerfile.shop)
- [`lab/browser`](lab/browser)
- [`lab/make_certs.sh`](lab/make_certs.sh)
- [`lab/price_check.py`](lab/price_check.py)
- [`lab/shop.conf`](lab/shop.conf)
- [`lab/site/index.html`](lab/site/index.html)
- [`lab/site/prices.json`](lab/site/prices.json)

## Commands, in the order the video runs them

### Works in the browser, not in curl

```sh
# ana@laptop:~$
curl https://shop.test
browser https://shop.test
# ben@ben-pc:~$
python3 price_check.py
```

### The usual fix: the full chain

```sh
# ana@shop:~$
grep ssl_certificate /etc/nginx/sites-enabled/shop
ls /etc/ssl/shop
grep -c BEGIN /etc/ssl/shop/cert.pem /etc/ssl/shop/fullchain.pem
sudo sed -i 's|/cert.pem|/fullchain.pem|' /etc/nginx/sites-enabled/shop
grep ssl_certificate /etc/nginx/sites-enabled/shop
sudo nginx -t
sudo nginx -s reload
# ben@ben-pc:~$
curl https://shop.test
python3 price_check.py
```

### What the server sends

```sh
# ben@ben-pc:~$
openssl s_client -connect shop.test:443 </dev/null 2>/dev/null | grep -E 's:|i:|Verify'
```

### Why the browser worked

```sh
# ana@shop:~$
openssl x509 -in /etc/ssl/shop/cert.pem -noout -ext authorityInfoAccess
sudo tail -n 2 /var/log/nginx/access.log | cut -d'"' -f2
```

### The fix that only fixes you

```sh
# ana@laptop:~$
curl -s http://ca.test/issuing-ca.crt | openssl x509 -inform der > issuing.crt
sudo cp issuing.crt /usr/local/share/ca-certificates/
sudo update-ca-certificates
curl https://shop.test
# ben@ben-pc:~$
curl https://shop.test
```

### Two fixes to avoid

```sh
# ben@ben-pc:~$
curl https://ca.test
curl -k https://ca.test
# ana@shop:~$
cd /etc/ssl/shop && cat chain.pem cert.pem | sudo tee backwards.pem >/dev/null
# ana@shop:/etc/ssl/shop$
sudo sed -i 's|/fullchain.pem|/backwards.pem|' /etc/nginx/sites-enabled/shop
sudo nginx -t
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
