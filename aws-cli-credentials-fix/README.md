# How to Fix AWS CLI 'Unable to Locate Credentials'

Video: https://youtu.be/GUt_DcLb010  
Written version: https://cloudexplainers.com/how-to-fix-aws-cli-unable-to-locate-credentials/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/boxoffice/backup.sh`](lab/boxoffice/backup.sh)
- [`lab/boxoffice/sales.csv`](lab/boxoffice/sales.csv)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### Twelve places, all empty

```sh
# ana@boxoffice:~$
aws s3 ls
aws s3 ls --debug 2>&1 | grep -o 'credentials via: .*'
aws s3 ls --debug 2>&1 | grep -c 'credentials via'
```

### The usual fix, and its trap

```sh
# ana@boxoffice:~$
aws configure list
aws configure --profile theatre
cat ~/.aws/credentials
aws s3 ls
aws configure list
aws configure list-profiles
aws s3 ls --profile theatre
AWS_PROFILE=theater aws s3 ls
echo 'export AWS_PROFILE=theatre' >> ~/.bashrc
export AWS_PROFILE=theatre
aws configure list
aws s3 ls
unset AWS_ACCESS_KEY_ID
```

### Works by hand, fails at 2 AM

```sh
# ana@boxoffice:~$
cat backup.sh
./backup.sh
crontab -l
cat backup.log
grep -E '^(HOME|AWS_)' cron-env.txt
grep -n AWS_PROFILE ~/.bashrc
crontab -l
tail -n 1 backup.log
aws s3 ls s3://riverside-box-office/sales/
```

### Fails with sudo

```sh
# ana@boxoffice:~$
aws s3 cp /var/log/boxoffice.log s3://riverside-box-office/logs/
sudo aws s3 cp /var/log/boxoffice.log s3://riverside-box-office/logs/
sudo env | grep -E '^(HOME|AWS_)'
sudo cat /var/log/boxoffice.log | aws s3 cp - s3://riverside-box-office/logs/boxoffice.log
aws s3 ls s3://riverside-box-office/logs/
```

### Before you trust a script

```sh
# ana@boxoffice:~$
aws sts get-caller-identity
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
