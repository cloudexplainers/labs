"""The steps Python's interpreter runs for one line: total += p."""
import dis
def add(total, p):
    total += p
    return total
dis.dis(add)
