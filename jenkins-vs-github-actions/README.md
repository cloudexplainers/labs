# DevOps Pipelines: Jenkins vs GitHub Actions

Video: https://youtu.be/N00jCdV7lPg  
Written version: https://cloudexplainers.com/devops-pipelines-jenkins-vs-github-actions/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/app/.github/workflows/ci.yml`](lab/app/.github/workflows/ci.yml)
- [`lab/app/Jenkinsfile`](lab/app/Jenkinsfile)
- [`lab/app/slots.py`](lab/app/slots.py)
- [`lab/app/test_slots.py`](lab/app/test_slots.py)
- [`lab/jenkins/Dockerfile`](lab/jenkins/Dockerfile)
- [`lab/jenkins/casc.yaml`](lab/jenkins/casc.yaml)
- [`lab/jenkins/plugins.txt`](lab/jenkins/plugins.txt)
- [`lab/laptop/Dockerfile`](lab/laptop/Dockerfile)
- [`lab/runner/Dockerfile`](lab/runner/Dockerfile)
- [`lab/staging/Dockerfile`](lab/staging/Dockerfile)
- [`lab/staging/serve.py`](lab/staging/serve.py)
- [`lab/steps/bug/slots.py`](lab/steps/bug/slots.py)
- [`lab/steps/fix/.github/workflows/ci.yml`](lab/steps/fix/.github/workflows/ci.yml)
- [`lab/steps/fix/slots.py`](lab/steps/fix/slots.py)

## Commands, in the order the video runs them

### The same push, twice

```sh
# ana@laptop:~/salon$
git remote -v
git push -q office main
git push -q github main
gh run view 43741177768 --log-failed | cut -f3- | cut -d' ' -f2- | grep -E '^curl:|error'
curl -sn http://jenkins:8080/job/salon/1/consoleText | grep -E '^Started|passed|failed|deployed|Finished'
```

### Two files, one plan

```sh
# ana@laptop:~/salon$
cat Jenkinsfile
cat .github/workflows/ci.yml
```

### Where the job runs

```sh
# ana@laptop:~/salon$
gh run view 43741177768 --log | cut -f3- | cut -d' ' -f2- | grep -E '^[0-9]+ CPUs'
curl -sn http://jenkins:8080/job/salon/1/consoleText | grep -E '^[0-9]+ CPUs'
```

### A change the tests catch

```sh
# ana@laptop:~/salon$
git diff
curl -sn http://jenkins:8080/job/salon/2/consoleText | grep -E '^(E +assert|FAILED|[0-9]+ failed|Finished)'
gh run view 43741281007 --log-failed | cut -f3- | cut -d' ' -f2- | grep -E '^(E +assert|FAILED|[0-9]+ failed)'
```

### Getting both

```sh
# ana@laptop:~/salon$
git diff
gh run view 43741375602
gh run view 43741375602 --log | cut -f3- | cut -d' ' -f2- | grep -E '^staging:'
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
