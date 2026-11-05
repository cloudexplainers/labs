# Ana's laptop for P081 "Django vs FastAPI": a stock Ubuntu 24.04 with Python 3.12 from apt and one virtual
# environment (~/.venv, the PEP 668 way from P072) holding Django, Gunicorn, FastAPI and Uvicorn from PyPI.
# ~/django-shop starts empty (the demo runs startproject on camera); Ana's own files wait in ~/ready and are
# copied in off camera. ~/fastapi-shop holds her one FastAPI file.
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-venv curl ca-certificates procps \
 && rm -rf /var/lib/apt/lists/* \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash ana
USER ana
RUN python3 -m venv /home/ana/.venv \
 && /home/ana/.venv/bin/pip install --no-cache-dir -q django gunicorn fastapi uvicorn
ENV PATH=/home/ana/.venv/bin:$PATH VIRTUAL_ENV=/home/ana/.venv
RUN mkdir -p /home/ana/django-shop /home/ana/fastapi-shop /home/ana/ready
COPY --chown=ana:ana django/ /home/ana/ready/
COPY --chown=ana:ana fastapi/main.py /home/ana/fastapi-shop/main.py
COPY --chown=ana:ana hammer.py /home/ana/hammer.py
CMD ["sleep", "infinity"]
