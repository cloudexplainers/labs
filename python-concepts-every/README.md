# Every Python Concept for Beginners in 10 Minutes

Video: https://youtu.be/uGg8J7grQjw  
Written version: https://cloudexplainers.com/every-python-concept-for-beginners-in-10-minutes/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/ask.py`](lab/ask.py)
- [`lab/ask_safe.py`](lab/ask_safe.py)
- [`lab/line_total.py`](lab/line_total.py)
- [`lab/line_total_fixed.py`](lab/line_total_fixed.py)
- [`lab/order.py`](lab/order.py)
- [`lab/receipt.py`](lab/receipt.py)
- [`lab/shipping.py`](lab/shipping.py)
- [`lab/teas.py`](lab/teas.py)
- [`lab/typo.py`](lab/typo.py)

## Commands, in the order the video runs them

### Your first error

```sh
# ana@laptop:~/shop$
cat order.py
python3 order.py
```

### Variables and types

```sh
# ana@laptop:~/shop$
python3
>>> tins = 2
>>> tins + 1
>>> type(tins)
>>> type("2")
>>> type(6.5)
```

### Strings

```sh
>>> name = "Ana"
>>> f"{name} ordered {tins} tins"
>>> name.upper()
>>> len("Sencha")
```

### Lists

```sh
>>> teas = ["Sencha", "Assam", "Oolong"]
>>> teas[0]
>>> teas[1]
>>> teas[-1]
>>> teas.append("Earl Grey")
>>> len(teas)
>>> teas[4]
```

### Dictionaries

```sh
>>> prices = {"Sencha": 6.5, "Assam": 4.0}
>>> prices["Assam"]
>>> prices["Oolong"] = 8.0
>>> prices
>>> prices["Matcha"]
>>> prices.get("Matcha", 0)
```

### If and else

```sh
# ana@laptop:~/shop$
python3 shipping.py
python3 typo.py
```

### Loops

```sh
# ana@laptop:~/shop$
python3 teas.py
```

### Functions

```sh
# ana@laptop:~/shop$
cat line_total.py
python3 line_total.py
cat line_total_fixed.py
python3 line_total_fixed.py
```

### Errors

```sh
# ana@laptop:~/shop$
python3 ask.py
python3 ask_safe.py
```

### All eight together

```sh
# ana@laptop:~/shop$
cat receipt.py
python3 receipt.py
python3 receipt.py
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
