import sys
import numpy as np
import scipy.signal

grid = []

for line in sys.stdin:
    row = []
    line = line.strip()
    if line:
        for c in line:
            if c == "#":
                row.append(2)
            elif c == "L":
                row.append(1)
            elif c == ".":
                row.append(0)
    grid.append(row)

grid = np.array(grid)
seats_mask = grid > 0
adjacent_kernel = np.ones((3, 3), dtype=np.int8)
adjacent_kernel[1, 1] = 0


def progress(grid):
    occupied_mask = grid == 2
    neighbors = scipy.signal.convolve2d(
        occupied_mask.astype(np.int8), adjacent_kernel, mode="same"
    )
    changed = False

    m1 = (neighbors == 0) & seats_mask & ~occupied_mask
    changed = changed or np.any(m1)
    grid[m1] = 2

    m2 = (neighbors >= 4) & seats_mask & occupied_mask
    changed = changed or np.any(m2)
    grid[m2] = 1
    return grid, changed


steps = 0
while True:
    print(grid)
    grid, changed = progress(grid)
    if not changed:
        break
    steps += 1

print(steps)
print(np.count_nonzero(grid == 2))
