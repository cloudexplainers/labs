# P128's family PC: a stock Ubuntu 24.04 image with Ubuntu's own Python 3.12 and its venv module, sudo, and John's
# family recipe site project (lab/recipe-site). John may use sudo without a password (a lab shortcut, said in the
# brief). The six photos are plain gradients made at build time (make_photos.py). /var/www/recipes belongs to root, like a web server's folder. Packages come from PyPI on camera.
FROM python:3.12-slim AS photos
RUN pip install -q pillow
COPY make_photos.py /
RUN python /make_photos.py /photos

FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-venv sudo ca-certificates less \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash john \
 && echo 'john ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/john \
 && touch /home/john/.hushlogin \
 && mkdir -p /var/www/recipes
COPY --chown=john:john recipe-site /home/john/recipe-site
COPY --from=photos --chown=john:john /photos /home/john/recipe-site/photos
RUN chmod +x /home/john/recipe-site/build.py
CMD ["sleep", "infinity"]
