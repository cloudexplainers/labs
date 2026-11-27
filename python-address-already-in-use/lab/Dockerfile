# P175's lab image: a stock Ubuntu 24.04 standing in for a greenhouse's small computer. Ana and Ben each have a copy
# of the greenhouse's two Python programs in ~/greenhouse: dashboard.py (a Flask page with the bench temperatures,
# port 5000) and collector.py (Python's own socket module: it takes readings from the bench sensors on port 9000).
# The same image is the bench sensor box (sensor.py sends one reading and waits for "ok").
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends sudo python3 python3-flask iproute2 lsof procps \
      curl less nano ca-certificates \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash -G sudo ana && useradd -m -s /bin/bash ben \
 && echo 'ana ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/ana && chmod 440 /etc/sudoers.d/ana \
 && touch /home/ana/.hushlogin /home/ben/.hushlogin
COPY dashboard.py collector.py sensor.py /opt/greenhouse/
RUN for u in ana ben; do mkdir /home/$u/greenhouse && cp /opt/greenhouse/dashboard.py /opt/greenhouse/collector.py \
      /home/$u/greenhouse/ && chown -R $u:$u /home/$u/greenhouse; done
CMD ["sleep", "infinity"]
