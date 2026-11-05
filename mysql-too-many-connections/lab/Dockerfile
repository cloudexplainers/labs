FROM python:3.13-slim
RUN pip install --no-cache-dir PyMySQL==1.2.3 SQLAlchemy==2.1.8 && useradd -m -s /bin/bash ana
COPY --chown=ana:ana shop/ /home/ana/shop/
USER ana
WORKDIR /home/ana/shop
CMD ["sleep", "infinity"]
