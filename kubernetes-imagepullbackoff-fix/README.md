# How to Fix Kubernetes ImagePullBackOff Errors

Video: https://youtu.be/4cKTI4UaXeM  
Written version: https://cloudexplainers.com/how-to-fix-kubernetes-imagepullbackoff-errors/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/laptop/Dockerfile`](lab/laptop/Dockerfile)
- [`lab/registry/setup.sh`](lab/registry/setup.sh)
- [`lab/steps/app/Dockerfile`](lab/steps/app/Dockerfile)
- [`lab/steps/app/app.py`](lab/steps/app/app.py)
- [`lab/steps/app11/Dockerfile`](lab/steps/app11/Dockerfile)
- [`lab/steps/app11/app.py`](lab/steps/app11/app.py)
- [`lab/steps/app20/Dockerfile`](lab/steps/app20/Dockerfile)
- [`lab/steps/app20/app.py`](lab/steps/app20/app.py)
- [`lab/steps/cluster.yaml`](lab/steps/cluster.yaml)
- [`lab/steps/deployment-11.yaml`](lab/steps/deployment-11.yaml)
- [`lab/steps/deployment-20.yaml`](lab/steps/deployment-20.yaml)
- [`lab/steps/deployment-local.yaml`](lab/steps/deployment-local.yaml)
- [`lab/steps/deployment-registry.yaml`](lab/steps/deployment-registry.yaml)
- [`lab/steps/deployment-secret.yaml`](lab/steps/deployment-secret.yaml)
- [`lab/steps/deployment-typo.yaml`](lab/steps/deployment-typo.yaml)
- [`lab/steps/deployment.yaml`](lab/steps/deployment.yaml)

## Commands, in the order the video runs them

### The image is right there

```sh
# ana@taco-laptop:~/menu$
kubectl get pods
docker images menu
curl -s localhost:8080
kubectl apply -f deployment.yaml
```

### Read the reason first

```sh
# ana@taco-laptop:~/menu$
kubectl describe pod menu-d5f57d998-x6md2 | tail -n 5
kubectl describe pod menu-d5f57d998-x6md2 | grep 'Failed to pull'
```

### Only on your laptop

```sh
# ana@taco-laptop:~/menu$
kind load docker-image menu --name taco
docker exec taco-worker crictl images | grep menu
kubectl get pods
kubectl get deployment menu -o jsonpath='{..imagePullPolicy}{"\n"}'
docker tag menu menu:1.0
kind load docker-image menu:1.0 --name taco
kubectl apply -f deployment.yaml
kubectl rollout status deployment menu --timeout=120s
kubectl get pods
```

### A private registry

```sh
# ana@taco-laptop:~/menu$
docker login registry.taco.lan
docker tag menu:1.0 registry.taco.lan/menu:1.0
docker push -q registry.taco.lan/menu:1.0
grep image: deployment.yaml
kubectl apply -f deployment.yaml
kubectl get pods
kubectl get pods
kubectl describe pod menu-95db47759-4kxzp | grep 'Failed to pull'
kubectl create secret docker-registry taco-registry --from-file=.dockerconfigjson=$HOME/.docker/config.json
grep -A1 imagePullSecrets deployment.yaml
kubectl apply -f deployment.yaml
kubectl rollout status deployment menu --timeout=120s
kubectl get pods
```

### Retries, and a missing tag

```sh
# ana@taco-laptop:~/menu$
docker build -q -t registry.taco.lan/menu:1.1 app
grep image: deployment.yaml
kubectl apply -f deployment.yaml
kubectl describe pod menu-5dc898b969-nghgw | grep 'Failed to pull'
docker push -q registry.taco.lan/menu:1.1
kubectl get pods
grep image: deployment.yaml
kubectl describe pod menu-59cdd5b655-p994g | grep 'Failed to pull'
```

### Built for another processor

```sh
# ana@taco-laptop:~/menu$
docker buildx build -q --platform linux/amd64 -t registry.taco.lan/menu:2.0 --push app
kubectl apply -f deployment.yaml
kubectl describe pod menu-5ffd9bbb9f-mjhkr | grep 'Failed to pull'
kubectl get nodes -L kubernetes.io/arch
docker buildx build -q --platform linux/amd64,linux/arm64 -t registry.taco.lan/menu:2.0 --push app
kubectl get pods
kubectl exec deploy/menu -- wget -qO- 127.0.0.1:8080
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
