# How Amazon S3 Works

Video: https://youtu.be/z8y7Nmd4iME  
Written version: https://cloudexplainers.com/how-amazon-s3-works/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Commands, in the order the video runs them

### Uploaded, yet Access Denied

```sh
aws s3 mb s3://ana-tea-shop
aws s3 cp menu.txt s3://ana-tea-shop/ --no-progress
curl -s https://ana-tea-shop.s3.us-east-1.amazonaws.com/menu.txt | xmllint --format -
```

### Buckets and objects

```sh
aws s3api head-bucket --bucket ana-tea-shop
aws s3 cp kettle.jpg s3://ana-tea-shop/photos/2026/kettle.jpg --no-progress
aws s3 ls s3://ana-tea-shop/
aws s3api list-objects-v2 --bucket ana-tea-shop --query 'Contents[].[Key,Size]' --output text
aws s3api head-object --bucket ana-tea-shop --key photos/2026/kettle.jpg
md5 -q kettle.jpg
```

### Every request is checked

```sh
aws s3 cp s3://ana-tea-shop/menu.txt -
```

### Sharing one file safely

```sh
aws s3api get-public-access-block --bucket ana-tea-shop
URL=$(aws s3 presign s3://ana-tea-shop/menu.txt --expires-in 30)
curl -s "$URL"
curl -s "$URL" | xmllint --format -
```

### Versions

```sh
aws s3api put-bucket-versioning --bucket ana-tea-shop --versioning-configuration Status=Enabled
echo 'Copper kettle tea  4.50' > menu.txt
aws s3 cp menu.txt s3://ana-tea-shop/ --no-progress
aws s3 cp s3://ana-tea-shop/menu.txt -
aws s3api list-object-versions --bucket ana-tea-shop --prefix menu.txt --query 'Versions[].[VersionId,IsLatest]' --output text
aws s3 rm s3://ana-tea-shop/menu.txt
aws s3 ls s3://ana-tea-shop/
aws s3api list-object-versions --bucket ana-tea-shop --prefix menu.txt --query 'DeleteMarkers[].[VersionId,IsLatest]' --output text
aws s3api delete-object --bucket ana-tea-shop --key menu.txt --version-id ffQ27kz3B8QhZD06lBfmJJBILsQWaO_b
aws s3 cp s3://ana-tea-shop/menu.txt -
```

### Where the bytes live

```sh
aws s3 cp teapot.jpg s3://ana-tea-shop/photos/2026/teapot.jpg --storage-class GLACIER --no-progress
aws s3api list-objects-v2 --bucket ana-tea-shop --prefix photos/ --query 'Contents[].[Key,StorageClass]' --output text
aws s3api get-object --bucket ana-tea-shop --key photos/2026/teapot.jpg teapot-copy.jpg
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
