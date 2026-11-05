# Claude API vs Claude Pro: Why Your Subscription Doesn't Include It

Video: https://youtu.be/qQOyqEH43R4  
Written version: https://cloudexplainers.com/claude-api-vs-claude-pro-why-your-subscription-doesn-t-include-it/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/emails/torn-bag.txt`](lab/emails/torn-bag.txt)
- [`lab/on-plan`](lab/on-plan)
- [`lab/price`](lab/price)
- [`lab/summarize.py`](lab/summarize.py)

## Commands, in the order the video runs them

### Paid for Pro, and still an error

```sh
cat emails/torn-bag.txt
python3 summarize.py emails/torn-bag.txt
```

### Two products, one name

```sh
cat summarize.py
python3 summarize.py emails/torn-bag.txt
```

### What a plan pays for

```sh
unset ANTHROPIC_API_KEY
./on-plan emails/torn-bag.txt
```

### What one email costs

```sh
./price sonnet-5.5 800 61
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
