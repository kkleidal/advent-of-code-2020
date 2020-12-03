import sys
import numpy as np

grid = []
for line in sys.stdin:
    line = line.strip()
    if line:
        grid.append([c == "#" for c in line])
grid = np.array(grid)

count = 0
y = 0
x = 0
while y < grid.shape[0]:
    count += 1 if grid[y, x] else 0
    x = (x + 3) % grid.shape[1]
    y += 1
print(count)
