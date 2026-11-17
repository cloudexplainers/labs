# DevOps with Ansible Will Finally Make Sense After This

Video: https://youtu.be/MDl1VnVmlCc  
Written version: https://cloudexplainers.com/devops-with-ansible-will-finally-make-sense-after-this/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/ski/ansible.cfg`](lab/ski/ansible.cfg)
- [`lab/ski/group_vars/web.yml`](lab/ski/group_vars/web.yml)
- [`lab/ski/inventory.ini`](lab/ski/inventory.ini)
- [`lab/ski/site.yml`](lab/ski/site.yml)
- [`lab/ski/templates/index.html.j2`](lab/ski/templates/index.html.j2)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### Two servers, two answers

```sh
# ana@laptop:~/ski$
curl -s web1
curl -s web2
```

### The inventory

```sh
# ana@laptop:~/ski$
ls
cat inventory.ini
ansible web -m ping
ansible web -a 'nginx -v'
```

### The first playbook

```sh
# ana@laptop:~/ski$
cat site.yml
cat templates/index.html.j2
cat group_vars/web.yml
time ansible-playbook site.yml
ansible web3 -m setup -a 'filter=ansible_distribution*'
```

### Run it again

```sh
# ana@laptop:~/ski$
time ansible-playbook site.yml
```

### A change made by hand

```sh
# ana@laptop:~/ski$
curl -s web2
ansible-playbook site.yml --check --diff
curl -s web2
ansible-playbook site.yml
curl -s web2
```

### A line that looks harmless

```sh
# ana@laptop:~/ski$
ansible-playbook site.yml
ansible-playbook site.yml
curl -s web1/staff.txt
ansible-playbook site.yml
ansible-playbook site.yml
curl -s web1/staff.txt
```

### Restart only when needed

```sh
# ana@laptop:~/ski$
tail -13 site.yml
ansible-playbook site.yml
curl -sI web2 | grep X-Served
ansible-playbook site.yml
```

### A server that can't answer

```sh
# ana@laptop:~/ski$
ansible-playbook site.yml
```

### One change, every server

```sh
# ana@laptop:~/ski$
cat group_vars/web.yml
time ansible-playbook site.yml
for w in web1 web2 web3; do curl -s $w | tail -1; done
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
