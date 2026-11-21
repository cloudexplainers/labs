# Jim's laptop for P141 "How to Fix a Kubernetes Pod Stuck in CrashLoopBackOff": a stock Ubuntu 24.04 with systemd as PID 1,
# Ubuntu's own Docker (docker.io), and kind + kubectl downloaded from their official releases and checked against
# their published SHA-256. demo.sh runs it --privileged with its own cgroup namespace and fresh volumes for
# /var/lib/docker and /var/lib/containerd, so `kind create cluster` builds a real three-node cluster inside it.
FROM ubuntu:24.04
ARG KIND_V=v0.33.0
ARG KUBE_V=v1.37.2
ARG TARGETARCH
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends systemd systemd-sysv dbus sudo curl \
      iproute2 iptables procps ca-certificates docker.io docker-buildx socat openssl apache2-utils \
 && rm -f /usr/sbin/policy-rc.d \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash -G sudo,docker jim && echo 'jim:lab-only-Pool-lane-7' | chpasswd \
 && touch /home/jim/.hushlogin \
 && systemctl enable docker containerd \
 && systemctl mask getty@tty1.service console-getty.service
RUN cd /usr/local/bin \
 && curl -fsSLo kind https://github.com/kubernetes-sigs/kind/releases/download/$KIND_V/kind-linux-$TARGETARCH \
 && echo "$(curl -fsSL https://github.com/kubernetes-sigs/kind/releases/download/$KIND_V/kind-linux-$TARGETARCH.sha256sum | cut -d' ' -f1)  kind" | sha256sum -c \
 && curl -fsSLo kubectl https://dl.k8s.io/release/$KUBE_V/bin/linux/$TARGETARCH/kubectl \
 && echo "$(curl -fsSL https://dl.k8s.io/release/$KUBE_V/bin/linux/$TARGETARCH/kubectl.sha256)  kubectl" | sha256sum -c \
 && chmod +x kind kubectl
STOPSIGNAL SIGRTMIN+3
CMD ["/sbin/init"]
