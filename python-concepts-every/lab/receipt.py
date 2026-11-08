prices = {"Sencha": 6.5, "Assam": 4.0}

def line_total(tea, tins):
    return prices[tea] * tins

try:
    tins = int(input("Tins of each tea: "))
except ValueError:
    print("Not a number, so 1 tin each")
    tins = 1

total = 0
for tea in ["Sencha", "Assam"]:
    cost = line_total(tea, tins)
    print(f"{tea}: {cost:.2f}")
    total = total + cost

if total >= 20:
    print("Free shipping")
else:
    total = total + 3.5
    print("Shipping: 3.50")
print(f"Total: {total:.2f}")
