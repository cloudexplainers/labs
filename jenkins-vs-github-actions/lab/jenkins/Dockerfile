# Jenkins 2.580.2 LTS with the plugins a pipeline needs and the tools its jobs run (Python, pytest, curl).
FROM jenkins/jenkins:2.580.2-lts-jdk21
USER root
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-pytest curl && rm -rf /var/lib/apt/lists/*
USER jenkins
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN jenkins-plugin-cli -f /usr/share/jenkins/ref/plugins.txt
COPY casc.yaml /var/jenkins_home/casc.yaml
ENV CASC_JENKINS_CONFIG=/var/jenkins_home/casc.yaml JAVA_OPTS=-Djenkins.install.runSetupWizard=false
