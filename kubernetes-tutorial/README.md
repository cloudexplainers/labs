# Kubernetes: Full Tutorial for Beginners

Video: https://youtu.be/35H-yXgSf0A  
Written version: https://cloudexplainers.com/kubernetes-full-tutorial-for-beginners/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/laptop/Dockerfile`](lab/laptop/Dockerfile)
- [`lab/steps/app1/Dockerfile`](lab/steps/app1/Dockerfile)
- [`lab/steps/app1/app.py`](lab/steps/app1/app.py)
- [`lab/steps/app2/Dockerfile`](lab/steps/app2/Dockerfile)
- [`lab/steps/app2/app.py`](lab/steps/app2/app.py)
- [`lab/steps/cluster.yaml`](lab/steps/cluster.yaml)
- [`lab/steps/configmap-lunch.yaml`](lab/steps/configmap-lunch.yaml)
- [`lab/steps/configmap.yaml`](lab/steps/configmap.yaml)
- [`lab/steps/deployment-requests-typo.yaml`](lab/steps/deployment-requests-typo.yaml)
- [`lab/steps/deployment-requests.yaml`](lab/steps/deployment-requests.yaml)
- [`lab/steps/deployment-v2-config.yaml`](lab/steps/deployment-v2-config.yaml)
- [`lab/steps/deployment-v2.yaml`](lab/steps/deployment-v2.yaml)
- [`lab/steps/deployment.yaml`](lab/steps/deployment.yaml)
- [`lab/steps/service-typo.yaml`](lab/steps/service-typo.yaml)
- [`lab/steps/service.yaml`](lab/steps/service.yaml)

## Commands, in the order the video runs them

### Delete it, and it comes back

```sh
# ana@radio-laptop:~/radio$
kubectl get pods -l app=requests
kubectl delete pod requests-5d45889448-94rbt
kubectl get pods -l app=requests
```

### What Kubernetes does

```sh
# ana@radio-laptop:~/radio$
kubectl version --client
kind version
```

### A cluster on your laptop

```sh
# ana@radio-laptop:~/radio$
cat cluster.yaml
time kind create cluster --config cluster.yaml
kubectl get nodes
docker ps --format '{{.Names}}  {{.Image}}'
kubectl get pods -n kube-system
```

### Your first pod

```sh
# ana@radio-laptop:~/radio$
kubectl run hello --image=nginx:alpine
kubectl get pods
kubectl get pods -o custom-columns=POD:.metadata.name,STATUS:.status.phase,NODE:.spec.nodeName
kubectl describe pod hello | tail -n 6
kubectl logs hello | tail -n 2
kubectl exec hello -- nginx -v
kubectl delete pod hello
kubectl get pods
```

### Your app as an image

```sh
# ana@radio-laptop:~/radio$
cat app/Dockerfile
docker build -q -t requests:1.0 app
kind load docker-image requests:1.0 --name radio
```

### A Deployment: copies that come back

```sh
# ana@radio-laptop:~/radio$
cat deployment.yaml
kubectl apply -f deployment.yaml
kubectl get deployments
kubectl get replicasets
kubectl get pods -o custom-columns=POD:.metadata.name,STATUS:.status.phase,NODE:.spec.nodeName
kubectl delete pods --all
kubectl get pods
kubectl get pods
```

### Scaling, and losing a node

```sh
# ana@radio-laptop:~/radio$
kubectl scale deployment requests --replicas=6
kubectl get pods -o custom-columns=POD:.metadata.name,STATUS:.status.phase,NODE:.spec.nodeName
kubectl drain radio-worker --ignore-daemonsets
kubectl get pods -o custom-columns=POD:.metadata.name,STATUS:.status.phase,NODE:.spec.nodeName
kubectl get nodes
kubectl uncordon radio-worker
```

### A Service: one stable name

```sh
# ana@radio-laptop:~/radio$
kubectl run curl --image=curlimages/curl --command -- sleep infinity
cat service.yaml
kubectl apply -f service.yaml
kubectl get service requests
kubectl exec curl -- curl -sS requests/whoami
kubectl describe service requests | grep Endpoints
kubectl get pods --show-labels
kubectl apply -f service.yaml
kubectl describe service requests | grep Endpoints
for i in 1 2 3 4 5 6; do kubectl exec curl -- curl -s requests/whoami; done
kubectl port-forward service/requests 8080:80
```

### An update that fails twice

```sh
# ana@radio-laptop:~/radio$
grep ON_AIR app/app.py
docker build -q -t requests:2.0 app
grep image: deployment.yaml
kubectl apply -f deployment.yaml
kubectl get pods
kubectl exec curl -- curl -s requests/whoami
kubectl describe pod requests-5c8f69c89-c9hz8 | grep Failed | tail -n 2
kubectl rollout status deployment requests --timeout=5s
kind load docker-image requests:2.0 --name radio
kubectl get pods
kubectl exec curl -- curl -sS requests/whoami
kubectl logs requests-5c8f69c89-w6dhc --previous | tail -n 2
kubectl rollout undo deployment requests
kubectl get pods
kubectl exec curl -- curl -s requests/whoami
```

### Settings: ConfigMaps

```sh
# ana@radio-laptop:~/radio$
cat configmap.yaml
kubectl apply -f configmap.yaml
tail -n 6 deployment.yaml
kubectl apply -f deployment.yaml
kubectl rollout status deployment requests
kubectl exec curl -- curl -s requests | grep -o 'On air now: [^<]*'
kubectl apply -f configmap.yaml
kubectl exec deploy/requests -- printenv ON_AIR
kubectl rollout restart deployment requests
kubectl exec deploy/requests -- printenv ON_AIR
```

### Resources: the Pending pod

```sh
# ana@radio-laptop:~/radio$
tail -n 4 deployment.yaml
kubectl apply -f deployment.yaml
kubectl get pods
kubectl describe pod requests-7fbd678dd8-nvqst | grep FailedScheduling
kubectl get nodes -o custom-columns=NODE:.metadata.name,MEMORY:.status.allocatable.memory
kubectl apply -f deployment.yaml
kubectl rollout status deployment requests
kubectl get pods -o custom-columns=POD:.metadata.name,STATUS:.status.phase,NODE:.spec.nodeName
```

### Cleaning up

```sh
# ana@radio-laptop:~/radio$
kubectl delete -f deployment.yaml -f service.yaml -f configmap.yaml
kind delete cluster --name radio
docker ps
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
