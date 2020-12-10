import sys
import numpy as np


inputs = [0]
for line in sys.stdin:
    line = line.strip()
    if line:
        inputs.append(int(line))

inputs = sorted(inputs)
inputs.append(inputs[-1] + 3)
differences = np.convolve(inputs, [1, -1], mode="valid")
values, counts = np.unique(differences, return_counts=True)
diff_counts = {v: c for v, c in zip(values, counts)}
assert set(diff_counts).issubset({1, 2, 3})
print(diff_counts[1] * diff_counts[3])
