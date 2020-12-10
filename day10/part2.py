import sys
import numpy as np
from functools import lru_cache


inputs = [0]
for line in sys.stdin:
    line = line.strip()
    if line:
        inputs.append(int(line))

inputs = sorted(inputs)
inputs.append(inputs[-1] + 3)

# Memoized dynamic programming:
@lru_cache(maxsize=None)
def count_ways(i=0):
    if i == len(inputs) - 1:
        return 1
    j = i + 1
    ways = 0
    while j < len(inputs) and inputs[j] <= inputs[i] + 3:
        ways += count_ways(j)
        j += 1
    return ways


print(count_ways())
