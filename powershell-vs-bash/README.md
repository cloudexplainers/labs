# PowerShell vs Bash: Which One Should You Learn?

Video: https://youtu.be/gE82lqaOxQo  
Written version: https://cloudexplainers.com/powershell-vs-bash-which-one-should-you-learn/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/make_logs.sh`](lab/make_logs.sh)
- [`lab/shop/web/orders.json`](lab/shop/web/orders.json)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### What a shell is

```sh
PS C:\shop\logs> $PSVersionTable.PSVersion.ToString()
PS C:\shop\logs> Get-Command pwsh
```

### Text or objects?

```sh
# ana@laptop:~/shop/logs$
ls -l
ls -l | sort -k5 -n -r | head -3
ls -l | sort -k5 -n -r | head -3 | awk '{print $9}'
PS /home/ana/shop/logs> Get-ChildItem | Sort-Object Length -Descending | Select-Object -First 3 Name, Length
PS /home/ana/shop/logs> (Get-ChildItem | Sort-Object Length -Descending | Select-Object -First 3).Name
```

### Reading data from the web

```sh
# ana@laptop:~/shop/logs$
curl -s localhost:8080/orders.json | head -3
curl -s localhost:8080/orders.json | jq '.[] | select(.total > 20) | .id'
PS /home/ana/shop/logs> $orders = Invoke-RestMethod http://localhost:8080/orders.json
PS /home/ana/shop/logs> $orders[0]
PS /home/ana/shop/logs> $orders | Where-Object total -gt 20
PS /home/ana/shop/logs> $orders | Measure-Object total -Sum | Select-Object Count, Sum
```

### Where Bash wins

```sh
# ana@laptop:~/shop/logs$
time (for i in {1..10}; do bash -c exit; done)
time (for i in {1..10}; do pwsh -NoProfile -c exit; done)
PS /home/ana/shop/logs> Get-Alias ls
PS /home/ana/shop/logs> Get-Command ls | Format-List Name, CommandType, Source
PS /home/ana/shop/logs> (Get-Alias dir).Definition
PS C:\shop\logs> Get-Alias ls
PS C:\shop\logs> ls | Sort-Object Length -Descending | Select-Object -First 3 Name, Length
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
