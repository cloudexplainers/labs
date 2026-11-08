try:
    tins = int(input("How many tins? "))
    print("Tins:", tins)
except ValueError:
    print("Please type a number, like 2")
