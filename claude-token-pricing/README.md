# Claude Token Pricing Will Finally Make Sense After This

Video: https://youtu.be/7lvf0oq8wsk  
Written version: https://cloudexplainers.com/claude-token-pricing-will-finally-make-sense-after-this/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/ask`](lab/ask)
- [`lab/bill`](lab/bill)
- [`lab/bill.py`](lab/bill.py)
- [`lab/emails/torn-bag.txt`](lab/emails/torn-bag.txt)
- [`lab/handbook.md`](lab/handbook.md)
- [`lab/tokens`](lab/tokens)

## Commands, in the order the video runs them

### One message, almost a cent

```sh
./ask --chat priya "Hi, my House Blend bag arrived torn and half the beans spilled. Order KB-20417. Can you help?"
```

### What a token is

```sh
./tokens "Hello" "Kettle & Bean" "unbelievably" "1234567" "def total(price, qty):"
```

### Where the tokens came from

```sh
./tokens "Hi, my House Blend bag arrived torn and half the beans spilled. Order KB-20417. Can you help?"
./tokens --file handbook.md
./tokens --overhead
```

### Why output costs more

```sh
./bill sonnet-5.5 4 478 1476 348
```

### Why chats get more expensive

```sh
./ask --chat priya "A replacement, please. Could you make it Night Owl instead?"
./ask --chat priya "Thanks! Also, do you ship to Canada? My sister lives in Toronto."
./ask --chat priya "Great. How do subscriptions work?"
```

### Prompt caching

```sh
./bill sonnet-5.5 4 145 2334 212
./bill sonnet-5.5 2 1779 0 154
./ask "Do you ship to Canada?"
```

### Three more price levers

```sh
./bill --month 6000 sonnet-5.5 1781 154
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
