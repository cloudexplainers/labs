# How to Fix a Kubernetes Pod Stuck in CrashLoopBackOff

Video: https://youtu.be/20_hVb-TfCU  
Written version: https://cloudexplainers.com/how-to-fix-a-kubernetes-pod-stuck-in-crashloopbackoff/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/laptop/Dockerfile`](lab/laptop/Dockerfile)
- [`lab/steps/app/Dockerfile`](lab/steps/app/Dockerfile)
- [`lab/steps/app/app.py`](lab/steps/app/app.py)
- [`lab/steps/app/import.py`](lab/steps/app/import.py)
- [`lab/steps/app11/app.py`](lab/steps/app11/app.py)
- [`lab/steps/cluster.yaml`](lab/steps/cluster.yaml)
- [`lab/steps/deployment-11.yaml`](lab/steps/deployment-11.yaml)
- [`lab/steps/deployment-env.yaml`](lab/steps/deployment-env.yaml)
- [`lab/steps/deployment-mem.yaml`](lab/steps/deployment-mem.yaml)
- [`lab/steps/deployment-probe-fixed.yaml`](lab/steps/deployment-probe-fixed.yaml)
- [`lab/steps/deployment-probe.yaml`](lab/steps/deployment-probe.yaml)
- [`lab/steps/deployment.yaml`](lab/steps/deployment.yaml)
- [`lab/steps/import-deployment.yaml`](lab/steps/import-deployment.yaml)
- [`lab/steps/import-job.yaml`](lab/steps/import-job.yaml)

## Commands, in the order the video runs them

### It runs on the laptop

```sh
# jim@pool-laptop:~/lanes$
kubectl get pods
docker run -d --rm --name board -p 8080:8080 -e BOOKING_KEY="$(cat booking.key)" lanes:1.0
curl -s localhost:8080
```

### Missing variable: read the last run

```sh
# jim@pool-laptop:~/lanes$
kubectl logs lanes-f7669455-p2pwk --previous
kubectl describe pod lanes-f7669455-p2pwk | grep -A4 'Last State'
kubectl create secret generic booking --from-file=key=booking.key
grep -A5 env: deployment.yaml
kubectl apply -f deployment.yaml
kubectl rollout status deployment lanes --timeout=120s
kubectl get pods
```

### Out of memory: no error in the log

```sh
# jim@pool-laptop:~/lanes$
kubectl logs lanes-85bd8d6ff8-bzqz6 --previous
kubectl get pods
kubectl describe pod lanes-85bd8d6ff8-bzqz6 | grep -A4 'Last State'
grep -A2 limits: deployment.yaml
kubectl apply -f deployment.yaml
kubectl rollout status deployment lanes --timeout=180s
```

### Liveness probe on the wrong port

```sh
# jim@pool-laptop:~/lanes$
grep -A4 livenessProbe: deployment.yaml
kubectl get pods
kubectl logs lanes-865db9459d-8qwkg --previous
kubectl describe pod lanes-865db9459d-8qwkg | grep -i liveness
kubectl describe pod lanes-865db9459d-8qwkg | grep -A4 'Last State'
kubectl apply -f deployment.yaml
kubectl get pods
```

### A script that finishes: use a Job

```sh
# jim@pool-laptop:~/lanes$
kubectl get pods
kubectl logs import-8776d49f4-xh575 --previous
kubectl describe pod import-8776d49f4-xh575 | grep -A4 'Last State'
kubectl get pods
kubectl delete deployment import
head -n 2 import.yaml
kubectl apply -f import.yaml
kubectl get jobs
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
