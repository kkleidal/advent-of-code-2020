import sys
import numpy as np
import math
from functools import reduce

_, bus_list = list(sys.stdin)[:2]
constraints = [int(x) if x != "x" else None for x in bus_list.split(",")]

inputs = []
for offset, bus_id in enumerate(constraints):
    if bus_id is not None:
        inputs.append((bus_id, (bus_id - offset) % bus_id))

# Tuple of n, a pairs st. x_i = a_i (mod n_i) for all i.
inputs = sorted(inputs, reverse=True)

# Assuming all prime.
# Chinese remainder theorem. Search by sieving: https://en.wikipedia.org/wiki/Chinese_remainder_theorem
def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)


max_mod = reduce(lambda x, y: lcm(x, y[0]), inputs, 1)

addend, target = inputs[0]
for n, a in inputs:
    while target % n != a:
        target = (target + addend) % max_mod
    addend *= n
for n, a in inputs:
    assert target % n == a
    print("%d = %d (mod %d)" % (target, a, n))
print("Answer:", target)
