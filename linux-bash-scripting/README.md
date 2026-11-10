# Linux Bash Scripting: Full Tutorial for Beginners

Video: https://youtu.be/U2J9V9l8EjU  
Written version: https://cloudexplainers.com/linux-bash-scripting-full-tutorial-for-beginners/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/capture.py`](lab/capture.py)
- [`lab/home/readings/garden.csv`](lab/home/readings/garden.csv)
- [`lab/home/readings/north field.csv`](lab/home/readings/north field.csv)
- [`lab/home/readings/roof.csv`](lab/home/readings/roof.csv)
- [`lab/home/sensors.txt`](lab/home/sensors.txt)
- [`lab/home/style.css`](lab/home/style.css)
- [`lab/s1/report.sh`](lab/s1/report.sh)
- [`lab/s10/report.sh`](lab/s10/report.sh)
- [`lab/s3/count.sh`](lab/s3/count.sh)
- [`lab/s3b/count.sh`](lab/s3b/count.sh)
- [`lab/s4/count.sh`](lab/s4/count.sh)
- [`lab/s5/list.sh`](lab/s5/list.sh)
- [`lab/s5b/all.sh`](lab/s5b/all.sh)
- [`lab/s6/report.sh`](lab/s6/report.sh)
- [`lab/s8a/backup.sh`](lab/s8a/backup.sh)
- [`lab/s8b/backup.sh`](lab/s8b/backup.sh)
- [`lab/s8c/backup.sh`](lab/s8c/backup.sh)
- [`lab/s8d/backup.sh`](lab/s8d/backup.sh)
- [`lab/s9/list.sh`](lab/s9/list.sh)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### One command instead of five

```sh
# ana@station:~$
./backup.sh
ls /home/ana/backups
```

### A script is a file

```sh
# ana@station:~$
cat report.sh
ls
./report.sh
ls -l report.sh
chmod +x report.sh
ls -l report.sh
./report.sh
report.sh
echo $PATH
```

### Variables and quotes

```sh
# ana@station:~$
sensor = roof
sensor=roof
echo "Sensor: $sensor"
today=$(date +%F)
echo "Report for $today"
count=$(wc -l < readings/roof.csv)
echo "$count readings, $((24 - count)) missing"
file="north field.csv"
wc -l readings/$file
wc -l "readings/$file"
```

### Arguments and exit codes

```sh
# ana@station:~$
cat count.sh
chmod +x count.sh
./count.sh roof
./count.sh
ls readings/roof.csv
echo $?
ls readings/cellar.csv
echo $?
head -n 6 count.sh
./count.sh
echo $?
```

### Decisions with if

```sh
# ana@station:~$
[[ -f readings/roof.csv ]] && echo "the file is there"
[[ -f readings/cellar.csv ]] && echo "the file is there"
echo $?
name=""
[ $name = roof ] && echo yes
[[ $name = roof ]] && echo yes
tail -n 10 count.sh
./count.sh cellar
echo $?
./count.sh "north field"
echo $?
```

### Loops

```sh
# ana@station:~$
for f in readings/*.csv; do echo "$f"; done
cat list.sh
./list.sh
cat sensors.txt
cat all.sh
./all.sh
```

### Functions and pipes

```sh
# ana@station:~$
echo $((11.4 + 1))
sort -t, -k2 -n readings/roof.csv | tail -n 1
sort -t, -k2 -n readings/roof.csv | tail -n 1 | cut -d, -f2
head -n 14 report.sh
tail -n 3 report.sh
./report.sh
```

### Output and errors

```sh
# ana@station:~$
./all.sh > report.txt
cat report.txt
./all.sh > report.txt 2> errors.log
cat errors.log
./all.sh >> report.txt 2>> errors.log
wc -l report.txt errors.log
./count.sh cellar > /dev/null 2>&1
echo $?
```

### When a step fails

```sh
# ana@station:~$
cat backup.sh
ls -d /home/ana/*/
echo $?
ls *.gz
head -n 4 backup.sh
./backup.sh
echo $?
sed -n 3,5p backup.sh
./backup.sh
ls *.gz
sed -n 3p backup.sh
./backup.sh
echo $?
cat readings/cellar.csv | wc -l
echo $?
set -o pipefail
cat readings/cellar.csv | wc -l
echo $?
```

### Finding bugs

```sh
# ana@station:~$
bash -x count.sh "north field"
shellcheck list.sh
cat list.sh
shellcheck list.sh
echo $?
./list.sh
```

### The finished script

```sh
# ana@station:~$
head -n 11 report.sh
sed -n 13,26p report.sh
tail -n 14 report.sh
shellcheck report.sh
./report.sh
echo $?
ls /home/ana/backups
tar -tzf /home/ana/backups/readings-*.tar.gz
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
