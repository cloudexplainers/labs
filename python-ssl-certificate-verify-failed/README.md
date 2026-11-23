# How to Fix Python SSL: CERTIFICATE_VERIFY_FAILED Errors

Video: https://youtu.be/hvSvBkMJoAc  
Written version: https://cloudexplainers.com/how-to-fix-python-ssl-certificate-verify-failed-errors/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/farm/fetch.py`](lab/farm/fetch.py)
- [`lab/farm/requirements.txt`](lab/farm/requirements.txt)
- [`lab/farm/send_reading.py`](lab/farm/send_reading.py)
- [`lab/make_certs.py`](lab/make_certs.py)
- [`lab/portal/nginx.conf`](lab/portal/nginx.conf)
- [`lab/steps/truststore/fetch.py`](lab/steps/truststore/fetch.py)
- [`lab/steps/truststore/send_reading.py`](lab/steps/truststore/send_reading.py)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### The error and the words after the colon

```sh
# (.venv) chris@farm-pc:~/milk-tank$
python send_reading.py
```

### Quick fix: name the co-op's CA file

```sh
# (.venv) chris@farm-pc:~/milk-tank$
ls ~/Downloads
REQUESTS_CA_BUNDLE=~/Downloads/coop-root-ca.crt python send_reading.py
REQUESTS_CA_BUNDLE=~/Downloads/coop-root-ca.crt python fetch.py https://pypi.org
python fetch.py https://pypi.org
```

### Adding the CA to Ubuntu's list

```sh
# (.venv) chris@farm-pc:~/milk-tank$
curl https://portal.coop.lan/api/readings
sudo cp ~/Downloads/coop-root-ca.crt /usr/local/share/ca-certificates/
sudo update-ca-certificates
curl https://portal.coop.lan/api/readings
python send_reading.py
python -c 'import requests; print(requests.certs.where())'
grep -c 'BEGIN CERT' $(python -m certifi) /etc/ssl/certs/ca-certificates.crt
export REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
python send_reading.py
python fetch.py https://pypi.org
```

### truststore: Python uses the system's list

```sh
# (.venv) chris@farm-pc:~/milk-tank$
unset REQUESTS_CA_BUNDLE
pip install truststore
python send_reading.py
```

### pip behind the office's inspection proxy

```sh
# (.venv) sarah@office-laptop:~/milk-tank$
pip install requests
echo | openssl s_client -proxy proxy.coop.lan:8080 -connect pypi.org:443 2>/dev/null | openssl x509 -noout -issuer
sudo cp ~/Downloads/office-proxy-ca.crt /usr/local/share/ca-certificates/
sudo update-ca-certificates
pip install requests
```

### Expired, or the wrong name

```sh
# (.venv) chris@farm-pc:~/milk-tank$
python fetch.py https://tank.coop.lan
echo | openssl s_client -connect tank.coop.lan:443 2>/dev/null | openssl x509 -noout -enddate
python fetch.py https://portal
python fetch.py https://portal.coop.lan
```

### verify=False turns the check off

```sh
# (.venv) chris@farm-pc:~/milk-tank$
python fetch.py https://tank.coop.lan --no-verify
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
