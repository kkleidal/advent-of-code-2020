import sys
import numpy as np
from functools import reduce

grid = []
for line in sys.stdin:
    line = line.strip()
    if line:
        grid.append([c == "#" for c in line])
grid = np.array(grid)


def find_trees_for_slope(slope):
    dx, dy = slope
    count = 0
    y = 0
    x = 0
    while y < grid.shape[0]:
        count += 1 if grid[y, x] else 0
        x = (x + dx) % grid.shape[1]
        y += dy
    return count


slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
print(reduce(lambda x, y: x * y, map(find_trees_for_slope, slopes), 1))
