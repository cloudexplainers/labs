# How Kubernetes Works

Video: https://youtu.be/yQXZjsRHI-k  
Written version: https://cloudexplainers.com/how-kubernetes-works/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/deployment.yaml`](lab/deployment.yaml)
- [`lab/kind.yaml`](lab/kind.yaml)
- [`lab/service.yaml`](lab/service.yaml)
- [`lab/shop.py`](lab/shop.py)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### A pod comes back

```sh
# ana@laptop:~/shop$
kubectl get pods -l app=shop
kubectl delete pod shop-8f9c4c6b8-2rc5q
kubectl get pods -l app=shop
```

### The cluster

```sh
# ana@laptop:~/shop$
kubectl get nodes
kubectl get pods -n kube-system -o custom-columns=POD:.metadata.name,NODE:.spec.nodeName
```

### Desired state

```sh
# ana@laptop:~/shop$
cat deployment.yaml
kubectl apply -f deployment.yaml
sed -i 's/replicas: 3/replicas: 5/' deployment.yaml
grep replicas deployment.yaml
kubectl apply -f deployment.yaml
kubectl get pods -o custom-columns=POD:.metadata.name,NODE:.spec.nodeName -l app=shop
```

### The scheduler

```sh
# ana@laptop:~/shop$
kubectl events --for pod/shop-8f9c4c6b8-hp922
```

### On the node

```sh
# root@shop-worker:~#
pgrep -l 'kubelet|containerd$'
pgrep -a python3
```

### Controllers

```sh
# ana@laptop:~/shop$
kubectl get replicaset
```

### Services

```sh
# ana@laptop:~/shop$
kubectl get service shop
kubectl get endpointslices -l kubernetes.io/service-name=shop
kubectl exec client -- sh -c 'for i in 1 2 3 4 5 6; do wget -qO- http://shop; done'
```

### When a node dies

```sh
# ana@laptop:~/shop$
kubectl get nodes
kubectl exec client -- sh -c 'for i in 1 2 3 4 5 6; do wget -qO- http://shop; done'
kubectl get pods -l app=shop
kubectl get pods -o custom-columns=POD:.metadata.name,NODE:.spec.nodeName -l app=shop
```

### Rolling updates

```sh
# ana@laptop:~/shop$
kubectl set image deployment/shop web=kettle-shop:2.0
kubectl rollout status deployment/shop
kubectl exec client -- sh -c 'for i in 1 2 3 4 5 6; do wget -qO- http://shop; done'
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
