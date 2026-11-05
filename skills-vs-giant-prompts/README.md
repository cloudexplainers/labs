# Why AI Agent Skills Beat Giant Prompts

Video: https://youtu.be/ARBNbdi_GgY  
Written version: https://cloudexplainers.com/why-ai-agent-skills-beat-giant-prompts/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/agent`](lab/agent)
- [`lab/build`](lab/build)
- [`lab/grow`](lab/grow)
- [`lab/handbook/00-always.md`](lab/handbook/00-always.md)
- [`lab/handbook/01-late-orders.md`](lab/handbook/01-late-orders.md)
- [`lab/handbook/02-damaged-parcel.md`](lab/handbook/02-damaged-parcel.md)
- [`lab/handbook/03-refunds.md`](lab/handbook/03-refunds.md)
- [`lab/handbook/04-allergens.md`](lab/handbook/04-allergens.md)
- [`lab/handbook/05-wholesale.md`](lab/handbook/05-wholesale.md)
- [`lab/handbook/06-subscriptions.md`](lab/handbook/06-subscriptions.md)
- [`lab/handbook/07-gift-cards.md`](lab/handbook/07-gift-cards.md)
- [`lab/handbook/08-address-changes.md`](lab/handbook/08-address-changes.md)
- [`lab/handbook/09-grinder-warranty.md`](lab/handbook/09-grinder-warranty.md)
- [`lab/handbook/10-loyalty.md`](lab/handbook/10-loyalty.md)
- [`lab/handbook/11-data-requests.md`](lab/handbook/11-data-requests.md)
- [`lab/handbook/12-press.md`](lab/handbook/12-press.md)
- [`lab/mail/inbox.txt`](lab/mail/inbox.txt)
- [`lab/mail/refund.txt`](lab/mail/refund.txt)
- [`lab/mail/torn-bag.txt`](lab/mail/torn-bag.txt)
- [`lab/scripts/refund.py`](lab/scripts/refund.py)

## Commands, in the order the video runs them

### One email, twelve procedures

```sh
skills-lab$ ls
skills-lab$ ls handbook
```

### What the model reads

```sh
skills-lab$ ./agent --none "Reply with just: ok"
skills-lab$ ./agent --giant "Reply with just: ok"
skills-lab$ ./agent --skills "Reply with just: ok"
```

### The giant prompt

```sh
skills-lab$ wc -w giant/CLAUDE.md
skills-lab$ grep '^## ' giant/CLAUDE.md
skills-lab$ cat mail/torn-bag.txt
skills-lab$ ./agent --giant mail/torn-bag.txt
```

### What a skill is

```sh
skills-lab$ ls skills/.claude/skills
skills-lab$ cat skills/CLAUDE.md
skills-lab$ head -4 skills/.claude/skills/damaged-parcel/SKILL.md
```

### How a skill loads

```sh
skills-lab$ ./agent --skills mail/torn-bag.txt
```

### Scripts inside skills

```sh
skills-lab$ find skills/.claude/skills/refunds -type f
skills-lab$ ./agent --skills mail/refund.txt
```

### A busy morning

```sh
skills-lab$ cat mail/inbox.txt
skills-lab$ ./agent --skills mail/inbox.txt --no-reply
skills-lab$ ./agent --giant mail/inbox.txt --no-reply
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
