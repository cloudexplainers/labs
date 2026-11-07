# How to Fix a Leaked Gemini API Key

Video: https://youtu.be/a-9zojbjyj4  
Written version: https://cloudexplainers.com/how-to-fix-a-leaked-gemini-api-key/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/shop/ask`](lab/shop/ask)
- [`lab/shop/menu.txt`](lab/shop/menu.txt)
- [`lab/shop/usage`](lab/shop/usage)

## Commands, in the order the video runs them

### Your key is out

```sh
gitleaks git --redact -v
```

### What a leaked key lets anyone do

```sh
git log --oneline
```

### A new key, Gemini only

```sh
gcloud services api-keys list --format="table(displayName,restrictions.apiTargets[0].service)"
NEW=$(gcloud services api-keys create --display-name=shop-key-2 --api-target=service=generativelanguage.googleapis.com --format="value(response.uid)" 2>/dev/null)
echo $NEW
```

### Swap it in first

```sh
cp .env .env.old
echo "GEMINI_API_KEY=$(gcloud services api-keys get-key-string $NEW --format='value(keyString)')" > .env
git check-ignore -v .env .env.old
./ask "One calm sentence about Hojicha tea."
KEY_FILE=.env.old ./ask "One calm sentence about Genmaicha tea."
```

### Delete the leaked key

```sh
OLD=$(gcloud services api-keys list --filter='displayName~^shop-key$' --format="value(uid)")
gcloud services api-keys delete $OLD 2>&1 | grep -E "ERROR|displayName|deleteTime"
gcloud services api-keys delete $OLD --no-check-existing-usage 2>&1 | grep -E "ERROR|displayName|deleteTime"
KEY_FILE=.env.old ./ask "One calm sentence about Genmaicha tea."
./ask "One calm sentence about Silver Needle tea."
```

### Lock the new key down

```sh
OPEN=$(gcloud services api-keys create --display-name=test-open --format="value(response.uid)" 2>/dev/null)
echo "GEMINI_API_KEY=$(gcloud services api-keys get-key-string $OPEN --format='value(keyString)')" > .env.open
KEY_FILE=.env.open ./ask "One calm sentence about Sencha tea."
gcloud services api-keys update $NEW --api-target=service=generativelanguage.googleapis.com --allowed-ips=203.0.113.7 2>&1 | grep -E "ERROR|allowedIps|203"
gcloud services api-keys describe $NEW --format="yaml(displayName,restrictions)"
./ask "One calm sentence about Sencha tea."
```

### What was it used for?

```sh
./usage
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
